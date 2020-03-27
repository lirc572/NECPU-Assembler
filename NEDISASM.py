#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 14:53:12 2020

@author: lirc572
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

import sys
from pathlib import Path

def allignNum(ln, maxln):
    return (len(str(maxln)) - len(str(ln))) * " " + str(ln)

def allignOp(op):
    assert type(op) == type("OP")
    return op + " " * (4-len(op))

def allignReg(reg):
    reg = str(int(reg, 2))
    return "$" + reg + " " * (2-len(reg))

if __name__ == "__main__":
    if len(sys.argv) == 2:
        code = ""
        fname = sys.argv[1]
        with open(fname) as f:
            code = f.read()
        code = code.split("\n")
        while ("case" not in code[0]):
            code = code[1:]
        code = code[1:]
        while ("endcase" not in code[-1]):
            code = code[:-1]
        code = code[:-1]
        for i in range(len(code)):
            if "//" in code[i]:
                code[i] = code[i][:code[i].find("//")]
            code[i] = bin(int(code[i].split("'")[-1][1:-1]))[2:]
            if len(code[i]) < 32:
                code[i] = "0" * (32 - len(code[i])) + code[i]
        source = []
        line_number = 0
        number_of_lines = len(code)
        for line in code:
            op   = line[  :6 ]
            rd   = line[ 6:11]
            rs   = line[11:16]
            rt   = line[16:21]
            func = line[21:  ]
            imme = line[16:  ]
            inst = ""
            for key, value in Instructions.items():
                if value == int(op, 2):
                    inst = key
            if inst in ('SLT','SEQ','ADD','SUB','SLL','SRL','AND','OR','INV','XOR'):
                source.append(allignNum(line_number, number_of_lines) + " :  " + allignOp(inst) + " " + allignReg(rd) + ", " + allignReg(rs) + ", " + allignReg(rt) + " " + str(int(func, 2)))
            else:
                source.append(allignNum(line_number, number_of_lines) + " :  " + allignOp(inst) + " " + allignReg(rd) + ", " + allignReg(rs) + ", " + str(int(imme, 2)))
            line_number += 1
        current_dir = Path(Path.cwd())
        with open(current_dir / "disasmout.asm", "w") as f:
            f.write("//For reference only, operators are directly translated from respective fields\n")
            f.write("//All fields of an instruction are showed\n")
            f.write("//This is not a valid source file!\n")
            f.write("\n")
            for line in source:
                f.write(line + "\n")
