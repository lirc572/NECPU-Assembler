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
    "SLT"  : 5,
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

forward_jumps = []

def disassemble(code):
    bincode = bin(int(code[4:]))[2:]
    bincode = "0"*(32-len(bincode))+bincode
    op=bincode[:6]
    rd=bincode[6:11]
    rs=bincode[11:16]
    rt=bincode[16:21]
    func=bincode[21:]
    for k, v in Instructions.items():
        if v==int(op,2):
            return "%s $%d $%d $%d %d" % (k, int(rd,2), int(rs,2), int(rt,2), int(func,2))

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

def ImmedToNum(imme, LINE_NUMBER = 0):
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
        if len(instruction) > 0:
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
            return EncodeTypeB(op, RegToNum(instruction[1]), RegToNum(instruction[2]), ImmedToNum(instruction[3], line_number))
        elif op in ("LLI", "LUI", "BEQ", "BNE"):
            return EncodeTypeB(op, RegToNum(instruction[1]), RegToNum("$0"), ImmedToNum(instruction[2], line_number))
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
                c1 = EncodeTypeB("LUI", RegToNum("$31"), RegToNum("$0"), 65535)
                c2 = EncodeTypeB("LLI", RegToNum("$31"), RegToNum("$0"), 65535)
                c3 = EncodeTypeB("JMP", RegToNum("$31"), RegToNum("$0"), ImmedToNum("0"))
                forward_jumps.append((line_number, label))
                return (c1, c2, c3)
                #raise ValueError("Label '" + label + "' not found!")
        elif op == "LWI": #LOAD WORD IMMEDIATE
            c1 = ""
            c2 = EncodeTypeB("LLI", RegToNum(instruction[1]), RegToNum("$0"), bin(ImmedToNum(instruction[2], line_number))[2:][-16:])
            if len(bin(ImmedToNum(instruction[2], line_number))) > 18:
                c1 = EncodeTypeB("LUI", RegToNum(instruction[1]), RegToNum("$0"), bin(ImmedToNum(instruction[2], line_number))[2:][:-16])
            else:
                c1 = EncodeTypeB("LUI", RegToNum(instruction[1]), RegToNum("$0"), ImmedToNum("0"))
            return (c1, c2)
        elif op == "NOP":
            return "32'd0"
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
                if len(code) != 0 and len(c) == 3 and disassemble(c[2])[0] == "J" and disassemble(code[-1])[0] == "B":
                    tmp = code[-1]
                    code = code[:-1]
                    for i in c:
                        code.append(i)
                        line_number += 1
                    code = code[:-1] + [tmp] + [code[-1]]
                else:
                    for i in c:
                        code.append(i)
                        line_number += 1
            else:
                code.append(c)
                line_number += 1
    for j in forward_jumps:
        if j[1] in labels:
            if len(bin(labels[j[1]])) > 18:
                code[j[0]] = EncodeTypeB("LUI", RegToNum("$31"), RegToNum("$0"), bin(labels[j[1]])[2:][:-16])
            else:
                code[j[0]] = EncodeTypeB("LUI", RegToNum("$31"), RegToNum("$0"), ImmedToNum("0"))
            code[j[0]+1] = EncodeTypeB("LLI", RegToNum("$31"), RegToNum("$0"), bin(labels[j[1]])[2:][-16:])
        else:
            raise ValueError("Label '" + j[1] + "' not found!")
    return code

def dec2hex(dec):
    if dec[3] == 'd':
        return dec[:3] + 'h' + hex(int(dec[4:]))[2:]
    else:
        return dec

COMMENTBLOCK = '''
//////////////////////////////////////////////////////////////////////////////////
// Company: lirc572
// Engineer: lirc572
// 
// Create Date: 
// Design Name: NECPU
// Module Name: InstMem
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////
'''

import sys
from pathlib import Path

if __name__ == "__main__":
    assert len(sys.argv) in (3, 4)
    #0: pgm name
    #1: arg
    #2: src
    #3: output (optional)
    source = ""
    with open(Path(sys.argv[2])) as f:
        source = f.read()
    code = Assembler(source)
    if sys.argv[1] == "-v":
        out_dir = Path(sys.argv[2]).name.split(".")[0] + ".v"
        if len(sys.argv) == 4:
            current_dir = Path(Path.cwd())
            out_dir = current_dir / sys.argv[3]
        print(out_dir)
        with open(out_dir, "w") as f:
            f.write("`timescale 1ns / 1ps\n")
            f.write(COMMENTBLOCK)
            f.write("module instMem (\n")
            f.write("    input  [31:0]  address,\n")
            f.write("    output reg [31:0] inst\n")
            f.write("  );\n")
            f.write("  always @ (address) begin\n")
            f.write("    inst = 32'd0;\n")
            f.write("    case (address)\n")
            line_number = 0
            for line in code:
                f.write("      %d: inst = " % (line_number,) + dec2hex(line) + ";\n")
                line_number += 1
            f.write("    endcase\n")
            f.write("  end\n")
            f.write("endmodule\n")






