# NECPU-Assembler

- Instructions:
  - Command line usage:
    - `NEASM.py [-v/-b] [source_dir] <[targer_dir]>`
      - -v: full Verilog module output
      - -b: bin output (not yet implemented)
  - Empty lines are allowed
  - immediate must be a valid Python integer literal or expression. Note that immediate must not contain any white space characters even if you put an expression!
  - immediate will be ealuated with `eval()` without safety checking of any sort, so please don't write anything weird here :>
  - Comments (starting with '//') can be put on an empty line or after a valid instruction
  - Don't use register 31 because it is reserved for the assembler for pseudo-instructions!

