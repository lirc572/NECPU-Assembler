#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

PIX0 = "LLI $1, %s\n"
PIX1 = "LLI $1, %s\nBEQ $1, 0\n"
SAVE = "LWI $0, %d\nSW $1, $0, 0\n"
LOADCHANGKUAN = "LWI $0, %d\nLUI $1, %s\nLLI $1, %s\nSW $1, $0, 0\n"

if __name__ == "__main__":
    addr = 2147499999         #first address stores dimension (upper * lower === len * wid)
    if len(sys.argv) > 3:
        addr = sys.argv[-3]
    PIX = PIX0
    if len(sys.argv) > 4:
        if "-m" in sys.argv:
            PIX = PIX1
    fn = sys.argv[-2]
    vn = sys.argv[-1]
    with open(vn, "w") as fv:
        f = open(fn)
        chang = f.readline()
        kuan  = f.readline()
        fv.write(LOADCHANGKUAN % (addr, chang, kuan))
        addr += 1
        lines = f.readlines()
        f.close()
        processed_lines = []
        for line in lines:
            processed_lines.append((addr, line[:-1]))
            addr += 1
        grouped_lines = {}
        for line in processed_lines:
            if line[1] in grouped_lines:
                grouped_lines[line[1]].append(line[0])
            else:
                grouped_lines[line[1]] = [line[0]]
        for line in grouped_lines:
            for addr in line:
                fv.write(PIX % (addr, line[:-1]))
            fv.write(SAVE)
