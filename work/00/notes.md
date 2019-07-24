Hardware Architect will produce a comparison file, the chip api, and the test
script.

The comparison file is like an oracle that the developers should be using to
ensure the correctness of their work against the spec. the test script are the 
test cases.

Examples of HDL
 - verilog
 - VHDL

Bus: a collection of bits, very useful compared to individual bits.
HDL provides notation for a bus.

a[15] is a bus of 15 bits, 
  - a[0] operates on the lsb (least significant bit (the right hand bit))

Can address a sub-bus through the following notation.
  Add16(a[0..7]=lsb, a[8..15]=msb, b=..., out=...);
