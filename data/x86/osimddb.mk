TARGETS_ALL += data/x86/all
TARGETS_PHONY += data/x86/all

DATA_X86_EXTENSIONS = mmx sse

data/x86/all: $(foreach isax,$(DATA_X86_EXTENSIONS),data/x86/$(isax)-parsed.yml)

data/x86/%-parsed.yml: data/x86/parse.py data/x86/extensions.yml sources/clang/Headers
	cd $(dir $<) && ./$(notdir $<) $* > $(notdir $@)
