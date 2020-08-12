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
However, there are some important differences.

 * I plan to integrate or link additional data, such as
   * Performance/timing data:
     * [uops.info](https://uops.info/) (x86 only, sadly)
     * [llvm-mca](https://www.llvm.org/docs/CommandGuide/llvm-mca.html)
   * Details about what instructions are generated.
   * Grouping similar functions (*i.e.*, the same operations but different
     vector size or element types).
   * Information on compiler support (like when an intrinsic was added,
     what flags are necessary, *etc.*)
   * Links to implementations in
     [SIMD Everywhere](https://github.com/simd-everywhere/simde) so you
     can see what a function actually does, and how to do something
     similar in other ISA extensions.
 * Support for more than just x86; Arm, POWER, WASM, *etc.*
 * Richer information about the APIs:
   * Information about valid ranges for different parameters.
   * How NaNs, infinitiies, etc., are handled.
   * Size of input data (*i.e.*, not just a pointer, but an N element
     array).

Since the data is permissively licensed you can use it for whatever you
want.  An obvious idea would be a web site somewhat similar to the
Intel Intrinsics Guide.

However, the original goal is to use it as a data source for generating
tests for SIMDe.

## License

Some information is derived from the Apache 2.0 licensed headers which
are distributed with clang.  I haven't made a decision on the license
for original content in this repository; Apache 2.0 would make a lot
of sense due to the data from clang, but I'm not sure how appropriate
it is for non-code.  I'll try to make a decision on this soon.
