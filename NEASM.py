#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 11:42:16 2020

@author: lirc572
"""

"""
Instructions:
    Command line usage:
        NEASM.py [-v/-b] [source_dir] <[targer_dir]>
            -v: full Verilog module output
            -b: bin output (not yet implemented)
    Empty lines are allowed
    immediate must be a valid Python integer literal or expression. Note that immediate must not contain any white space characters even if you put an expression!
    immediate will be ealuated with `eval()` without safety checking of any sort, so please don't write anything weird here :>
    Comments (starting with '//') can be put on an empty line or after a valid instruction
    Don't use register 31 because it is reserved for the assembler for pseudo-instructions!
    
"""

"""
Todo:
    Currently JUMP pseudo-instruction can only jump up (to a previous line)
        Scan the whole source for labels first so that jumping down can be achieved
"""

Instructions = {
    "NOP"  : 0,
    "LW"   : 1,
    "SW"   : 2,
    "LLI"  : 3,
    "LUI"  : 4,
    "SLI"  : 5,
    "SEQ"  : 6,
    "BEQ"  : 7,
    "BNE"  : 8,
    "ADD"  : 9,
    "ADDI" : 10,
    "SUB"  : 11,
    "SUBI" : 12,
    "SLL"  : 13,
    "SRL"  : 14,
    "AND"  : 15,
    "ANDI" : 16,
    "OR"   : 17,
    "ORI"  : 18,
    "INV"  : 19,
    "XOR"  : 20,
    "XORI" : 21,
    "JMP"  : 22
}

labels = {}

def ZeroExtend(num, width):
    if type(num) == type(520):
        num = bin(num)[2:]
    if type(num) != type('1000001000'):
        raise TypeError("Number " + str(num) + " is of wrong type")
    if len(num) > width:
        raise ValueError("Number " + str(num) + " is too long")
    return "0" * (width-len(num)) + num

def EncodeTypeA(inst, rd, rs, rt, func):
    inst = ZeroExtend(Instructions[inst.upper()], 6)
    rd   = ZeroExtend(rd, 5)
    rs   = ZeroExtend(rs, 5)
    rt   = ZeroExtend(rt, 5)
    func = ZeroExtend(func, 11)
    return "32'd%d" % (int(inst+rd+rs+rt+func, 2),)

def RegToNum(reg):
    assert type(reg) == type("520")
    assert reg[0] == "$"
    return int(reg[1:])

def ImmedToNum(imme):
    assert type(imme) == type("1314")
    return eval(imme)

def EncodeTypeB(inst, rd, rs, immediate):
    inst = ZeroExtend(Instructions[inst.upper()], 6)
    rd   = ZeroExtend(rd, 5)
    rs   = ZeroExtend(rs, 5)
    immediate = ZeroExtend(immediate, 16)
    return "32'd%d" % (int(inst+rd+rs+immediate, 2),)

def EncodeInst(instruction, line_number):
    if "//" in instruction:
        instruction = instruction[:instruction.find("//")]
    instruction = instruction.replace(",", " ")
    instruction = instruction.split()
    if len(instruction) == 0:
        return
    op = instruction[0]
    if ":" in op:
        labels[op[:-1]] = line_number
        instruction = instruction[1:]
        op = instruction[0]
    if len(instruction) == 0:
        return
    else:
        op = op.upper()
        if op in ("SLT", "SEQ", "ADD", "SUB", "SLL", "SRL", "AND", "OR", "XOR"):
            return EncodeTypeA(op, RegToNum(instruction[1]), RegToNum(instruction[2]), RegToNum(instruction[3]), 0)
        elif op in ("INV",):
            return EncodeTypeA(op, RegToNum(instruction[1]), RegToNum(instruction[2]), RegToNum("$0"), 0)
        elif op in ("LW", "SW", "ADDI", "SUBI", "ANDI", "ORI", "XORI"):
            return EncodeTypeB(op, RegToNum(instruction[1]), RegToNum(instruction[2]), ImmedToNum(instruction[3]))
        elif op in ("LLI", "LUI", "BEQ", "BNE"):
            return EncodeTypeB(op, RegToNum(instruction[1]), RegToNum("$0"), ImmedToNum(instruction[2]))
        elif op in ("JMP",):
            return EncodeTypeB(op, RegToNum(instruction[1]), RegToNum("$0"), ImmedToNum("0"))
        elif op == "JUMP": #pseudo-instruction
            label = instruction[1]
            if label in labels:
                c1 = ""
                c2 = EncodeTypeB("LLI", RegToNum("$31"), RegToNum("$0"), bin(labels[label])[2:][-16:])
                if len(bin(labels[label])) > 18:
                    c1 = EncodeTypeB("LUI", RegToNum("$31"), RegToNum("$0"), bin(labels[label])[2:][:-16])
                else:
                    c1 = EncodeTypeB("LUI", RegToNum("$31"), RegToNum("$0"), ImmedToNum("0"))
                c3 = EncodeTypeB("JMP", RegToNum("$31"), RegToNum("$0"), ImmedToNum("0"))
                return (c1, c2, c3)
            else:
                raise ValueError("Label '" + label + "' not found!")
        else:
            raise ValueError("Unknown instruction: '" + op + "'")

def Assembler(source):
    assert type(source) == type("love you~")
    source = source.split("\n")
    code = []
    line_number = 0
    for line in source:
        c = EncodeInst(line, line_number)
        if c != None:
            if type(c) == type(("not", "you")):
                for i in c:
                    code.append(i)
                    line_number += 1
            else:
                code.append(c)
                line_number += 1
    return code

import sys

if __name__ == "__main__":
    assert len(sys.argv) in (3, 4)
    #0: pgm name
    #1: arg
    #2: src
    #3: output (optional)
    source = ""
    with open(sys.argv[2]) as f:
        source = f.read()
    code = Assembler(source)
    if sys.argv[1] == "-v":
        out_dir = sys.argv[2].split(".")[0] + ".v"
        if len(sys.argv) == 4:
            out_dir = sys.argv[3]
        with open(out_dir, "w") as f:
            f.write("`define InstBusWidth  32\n")
            f.write("`define InstAddrBus   32\n")
            f.write("module instMem (\n")
            f.write("    input  [`InstAddrBus-1:0]  address,\n")
            f.write("    output reg [`InstBusWidth-1:0] inst\n")
            f.write("  );\n")
            f.write("  always @ (address) begin\n")
            f.write("    inst = 32'd0;\n")
            f.write("    case (address)\n")
            line_number = 0
            for line in code:
                f.write("      %d: inst = " % (line_number,) + line + ";\n")
            f.write("    endcase\n")
            f.write("  end\n")
            f.write("endmodule\n")






