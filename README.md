# Open SIMD Database

## Work In Progress

This repository isn't really ready for widespread use yet.  Feel free
to poke around, and obviously contributions are welcome, but you
probably shouldn't use it for anything serious yet.

## Overview

This repository contains machine-readable (YAML) data about SIMD APIs
and code used to generate that data.

The basic idea is a permissively licensed alternative to the XML data
which powers the
[Intel Intrinsics Guide](https://software.intel.com/sites/landingpage/IntrinsicsGuide/).
However, there are some important differences.  Specifically, I plan to integrate or link
additional data, such as

* Details about what instructions are generated.  This shouldn't be 
  too difficult; just generate trivial wrappers in C then compile to
  assembly.  Once we have that it should be much easier to pull in
  data from other sources.
* Performance/timing data:
  * [uops.info](https://uops.info/) (x86 only, sadly)
  * [llvm-mca](https://www.llvm.org/docs/CommandGuide/llvm-mca.html)
  * [uarch-bench](https://github.com/travisdowns/uarch-bench)?
* Grouping similar functions (*i.e.*, the same operations but different
  vector size or element types).  My current plan here is to parse
  intrinsic names to find candidates, then generate C code to verify
  that our expectations hold (e.g., the data from two _mm_add_ps
  calls matches the data from one _mm256_add_ps).
* Information on compiler support (like when an intrinsic was added,
  what flags are necessary, *etc.*).  This should just be a matter
  of attempting to compile trivial wrappers using different compilers.
* Links to implementations in
  [SIMD Everywhere](https://github.com/simd-everywhere/simde) so you
  can see what a function actually does, and how to do something
  similar in other ISA extensions.
  * Longer term it may be possible to encode some of this information
    directly in this project, but it's not a high priority for me since
    looking in SIMDe suits me just fine.
* Support for more than just x86 (Arm, POWER, WASM, *etc.*)
* Richer information about the APIs:
  * Information about valid ranges for different parameters.  Again,
    this can be determined by trying to compile with different
    parameters.
  * How NaNs, infinitiies, etc., are handled.  Again, this can be
    determined experimentally.
  * Size of input data (*i.e.*, not just a pointer, but an N element
    array).  This will probably need to be added manually :(
  * Alignment requirements of pointer types (and arrays).  This will
    probably need to be added manually as well.
* Long term: documentation.  This would be a *ton* of work and would
  have to be done manually.  Some could be shared thanks to grouping
  functions, but it's still a lot of work.

Since the data is permissively licensed you can use it for whatever you
want.  An obvious idea would be a web site somewhat similar to the
Intel Intrinsics Guide.  However, the original goal is to use it as a
data source for generating tests for SIMDe, though I do have several
other ideas.

It's also worth noting that I plan to accept contributions just like
any open source project.  If you have some data that you'd like
integrated, or an idea of how to generate it, you're free to extend
the project to include it.  As long as the license is acceptable and
the data is useful, there is an excellent chance 

## License

Some information is derived from the Apache 2.0 licensed headers which
are distributed with clang.  I haven't made a decision on the license
for original content in this repository; Apache 2.0 would make a lot
of sense due to the data from clang, but I'm not sure how appropriate
it is for non-code.  I'll try to make a decision on this soon.
