#!/usr/bin/python3

# Yes, this is a mess.  I didn't really have a fully developed plan
# when I wrote this; it's basically a proof of concept that I'm too
# lazy to rewrite.  If anyone wants to clean this up I'd be willing
# to accept patches.

import re, mmap, sys, yaml, os

class Type:
  def parse(self, str):
    components = []
    for component in str.split(' '):
      component = component.strip()

      components.append(component)

    baseType = None
    for part in components:
      if part == 'const':
        self.isConst = True
      elif re.match('^\*+$', part):
        self.pointer += len(part)
      else:
        if baseType != None:
          baseType = baseType + ' ' + part
        else:
          baseType = part

    self.baseType = baseType

  def __init__(self):
    self.isConst = False
    self.pointer = 0
    self.baseType = None


class Arg:
  def __init__(self):
    self.name = None
    self.type = None

  def parse(self, str):
    components = list(map(lambda str: str.strip(), str.split(' ')))

    self.name = components[-1]
    components = components[0:-1]

    while self.name.startswith('*'):
      components.append('*')
      self.name = self.name[1:]

    if self.name.startswith('__'):
      self.name = self.name[2:]

    if len(components) != 0:
      self.type = Type()
      self.type.parse(' '.join(components))

  @staticmethod
  def parse_multiple(str):
    if str == None:
      return None

    str = str.strip()
    if str == '':
      return None

    args = str.split(',');
    args = list(map(lambda str: str.strip(), args))

    res = []
    for arg in args:
      a = Arg()
      a.parse(arg)
      res.append(a)

    return res


class Func:
  def __init__(self):
    self.name = None
    self.ret = None
    self.args = []

  def parse(self, name, rettype, args):
    self.name = name

    if rettype == None:
      self.ret = None
    else:
      self.ret = Type()
      self.ret.parse(rettype)

    self.args = Arg.parse_multiple(args)

class FuncStore:
  def __init__(self):
    self.data = {}

  def get(self, name):
    return self.data[name]

  def add(self, func):
    if ('' in self.data):
      print(func.name + " already exists");
      return

    self.data[func.name] = func

funcStore = FuncStore()

extensionData = None
overrideData = {}

with open('extensions.yml') as fp:
  for extension in yaml.safe_load(fp):
    if extension["id"] == sys.argv[1]:
      extensionData = extension
      break

  if extensionData == None:
    sys.stderr.write("Unable to find extension data\n")
    exit(1)

try:
  with open(extension['id'] + '-override.yml') as fp:
    for funcData in yaml.safe_load(fp):
      overrideData[funcData['name']] = funcData
except FileNotFoundError:
  pass

with open(os.path.join('..', '..', 'sources', 'clang', 'Headers', extension['header']), 'r') as fp:
  data = fp.read()

  # Find normal functions
  mo = re.findall('^static __inline__ (.+) __DEFAULT_FN_ATTRS([_A-Z0-9]+)?\n(_mm(256|512)?_[a-zA-Z0-9_]+)\\s*\(([^\\)]*)\)', data, re.MULTILINE)
  for m in mo:
    func = Func()
    func.parse(m[2], m[0], m[4])
    funcStore.add(func)

  # Clang includes documentation of the intrinsics which 
  mo = re.findall('^\s*#define\s+(_mm(256|512)?_([a-zA-Z0-9_]+))\(([^\)]+)', data.replace('\\\n', ''), re.MULTILINE)
  for m in mo:
    func = Func()
    func.parse(m[0], None, m[3])
    funcStore.add(func)

# It would probably make more sense to handle the override data when we
# parse the headers instead of while we're generating the output.
def type_to_yaml(dataType):
  if dataType == None:
    return {}
  
  argData = {}
  if dataType.baseType != None:
    argData["type"] = dataType.baseType
  if dataType.pointer != 0:
    argData["pointer"] = dataType.pointer
  if dataType.isConst:
    argData["const"] = True

  return argData

functions = []
for name in sorted(funcStore.data):
  funcData = { 'name': name }
  if name in overrideData:
    funcData = overrideData[name]

  func = funcStore.get(name)

  returnData = None
  if 'return' in funcData:
    returnData = funcData['return']
  else:
    returnData = {}

  ret = func.ret
  if ret != None:
    if (not 'type' in returnData) and (ret.baseType != None):
      returnData['type'] = ret.baseType
    if (not 'pointer' in returnData) and (ret.pointer != 0):
      returnData['pointer'] = ret.pointer

  if len(returnData) != 0:
    funcData['return'] = returnData

  if 'arguments' in funcData:
    argsData = funcData["arguments"]

    assert len(argsData) == len(func.args)

    for argNum in range(0, len(argsData)):
      arg = type_to_yaml(func.args[argNum].type)

      if (not 'name' in argsData) and ('name' in arg):
        argsData['name'] = arg['name']
      if (not 'type' in argsData) and ('type' in arg):
        argsData['type'] = arg['type']
      if (not 'const' in argsData) and ('const' in arg):
        argsData['const'] = arg['const']
      
      if (not 'array' in argsData):     
        if (not 'pointer' in argsData) and ('pointer' in arg):
          argsData['pointer'] = arg['pointer']
  else:
    args = func.args
    argsData = []

    for arg in args:
      argData = type_to_yaml(arg.type)
        
      if arg != None:
        argData['name'] = arg.name

      argsData.append(argData)

    if len(argsData) > 0:
      funcData['arguments'] = argsData

  functions.append(funcData)

yaml.dump(functions, sys.stdout)
