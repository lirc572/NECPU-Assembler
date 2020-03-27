# NECPU-Assembler

## Assembler

### How-To

- Command line usage:
  - `NEASM.py [-v/-b] [source_dir] <[targer_dir]>`
  - -v: full Verilog module output
  - -b: bin output (not yet implemented)
- Empty lines are allowed
- immediate must be a valid Python integer literal or expression. Note that immediate must not contain any white space characters even if you put an expression!
- immediate will be ealuated with `eval()` without safety checking of any sort, so please don't write anything weird here :>
- Comments (starting with '`//`') can be put on an empty line or after a valid instruction
- Don't use register 31 because it is reserved for the assembler for pseudo-instructions!

### Architecture Description

The **NECPU** is a 32-bit general purpose register architecture processor with the specifications below. Registers `$rs`, `$rt`, and `$rd` are placeholders for actual general purpose registers `$0`, `$1`, `$2`, ..., `$31`, each holding a 32-bit value. `immediate` refers to an immediate value (constant) and `label` refers to label in the instruction corresponding to a specific line in the code. All *immediates* are given as 16-bit unsigned values. Whenever an *immediate* is used as an operand with a register as the other operand, the *immediate* is zero-extended to 32-bit before computation. All *labels* will be converted into actual addresses using direct addressing mode.

**NECPU** can accomodate up to 4294967296 (2^32) addressable memory where each memory location holds 4 bytes (32 bits). **NECPU** is word (4 bytes) addressable. (It is not byte addressable!)

Every instruction of **NECPU** takes exactly one clock cycle to complete. Hence, the time taken of a code snippet can easily be calculated.

#### Instruction Set

We will use the following convension to simplify our description:

- Given a register `$r`, the content of the register `$r` is given as `R[$r]`.
- Given a memory location `addr`, the content at the memory location `addr` is `M[addr]`.
- `PC` is the program counter which is a special register that holds the address of the instruction currently being executed.

Instruction Format             | Name                 | Operation
------------------------------ | -------------------- | ----------------------------------
NOP                            | No-Op                | Do nothing
LW   `$rd`, `$rs`, `immediate` | Load Word            | `R[$rd]` = `M[R[$rs] + immediate]`
SW   `$rd`, `$rs`, `immediate` | Store Word           | `M[R[$rs] + immediate]` = `R[$rd]`
LLI  `$rd`, `immediate`        | Load Lower Immediate | `R[$rd][15:0]` = `immediate`
LUI  `$rd`, `immediate`        | Load Upper Immediate | `R[$rd][31:16]` = `immediate`
SLT  `$rd`, `$rs`, `$rt`       | Set Less Than        | `R[$rd]` = `R[$rs]` <  `R[$rt]`
SEQ  `$rd`, `$rs`, `$rt`       | Set Equal            | `R[$rd]` = `R[$rs]` == `R[$rt]`
BEQ  `$rd`, `immediate`        | Branch On Equal      | `PC` = `PC` + (`R[$rd]` == `immediate` ? 2 : 1)
BNE  `$rd`, `immediate`        | Branch On Not Equal  | `PC` = `PC` + (`R[$rd]` != `immediate` ? 2 : 1)
ADD  `$rd`, `$rs`, `$rt`       | Add                  | `R[$rd]` = `R[$rs]` + `R[$rt]`
ADDi `$rd`, `$rs`, `immediate` | Add immediate        | `R[$rd]` = `R[$rs]` + `immediate`
SUB  `$rd`, `$rs`, `$rt`       | Subtract             | `R[$rd]` = `R[$rs]` - `R[$rt]`
SUBi `$rd`, `$rs`, `immediate` | Subtract Immediate   | `R[$rd]` = `R[$rs]` - `immediate`
SLL  `$rd`, `$rs`, `$rt`       | Shift Left Logical   | `R[$rd]` = `R[$rs]` << `R[$rt]`
SRL  `$rd`, `$rs`, `$rt`       | Shift Right Logical  | `R[$rd]` = `R[$rs]` >> `R[$rt]`
AND  `$rd`, `$rs`, `$rt`       | And                  | `R[$rd]` = `R[$rs]` & `R[$rt]`
ANDi `$rd`, `$rs`, `immediate` | And Immediate        | `R[$rd]` = `R[$rs]` & `immediate`
OR   `$rd`, `$rs`, `$rt`       | Or                   | `R[$rd]` = `R[$rs]` | `R[$rt]`
ORi  `$rd`, `$rs`, `immediate` | Or Immediate         | `R[$rd]` = `R[$rs]` | `immediate`
INV  `$rd`, `$rs`              | Invert               | `R[$rd]` = ~ `R[$rs]`
XOR  `$rd`, `$rs`, `$rt`       | Xor                  | `R[$rd]` = `R[$rs]` ^ `R[$rt]`
XORi `$rd`, `$rs`, `immediate` | Xor Immediate        | `R[$rd]` = `R[$rs]` ^ `immediate`
JMP  `$rd`                     | Unconditional Jump   | `PC` = `R[$rd]`

#### Instruction Encoding

![Instruction Encoding](https://github.com/lirc572/NECPU/raw/master/necpu_encoding.png "Instruction Encoding")

- Type A
  - SLT
  - SEQ
  - ADD
  - SUB
  - SLL
  - SRL
  - AND
  - OR
  - INV (`$rt` ignored)
  - XOR
- Type B
  - LW
  - SW
  - LLI (`$rs` ignored)
  - LUI (`$rs` ignored)
  - BEQ (`$rs` ignored)
  - BNE (`$rs` ignored)
  - ADDi
  - SUBi
  - ANDi
  - ORi
  - XORi
  - JMP (can also put under type A since only `$rd` is used)

Note that the `BEQ` and `BNE` instructions of **NECPU** differ from those of **MIPS**:

- **NECPU**'s `BEQ` and `BNE` instructions compare a register's value with an `immediate`, while **MIPS** compares the values of two registers.
- **NECPU**'s `BEQ` and `BNE` instructions can only skip the next **one** instruction if the condition is satisfied.

### Pseudo-Instructions

- **JUMP** (unstable)
  - `JUMP [label]`
  - `JUMP` instruction complements the native `JMP` instruction by accepting a label instead of a raw memory address. It simplifies the programming experience.
  - To create a label, put `[label]:` before the instruction you want to jump to. The label can be any valid string.
  - **Currently JUMP pseudo-instruction only supports jumping backwards (to a line that the assembler has already processed at the point)**
- **LWI** - Load Word Immediate
  - `LWI $rd, immediate`
  - `LWI` basically combines `LLI` and `LUI`
  - `immediate` here is a 32-bit constant value (zero-extended)

### To-Do

- Implement `.data` directive to support preloading data into the ROM.
  - Support loading external files into ROM (in the format of bin or bmp)
- **LA** (Load Address) pseudo-instruction to load the address of variable defined in the `.data` section

## Disassembler

*The disassembler is for the purpose of debugging only.*

### How-To

- Command line usage:
  - `NEDISASM.py [verilog_instruction_rom_file_dir]`
  - The disassembled file `disasmout.asm` will be created in the current directory

