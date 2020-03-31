#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

if __name__ == '__main__':
    f1 = sys.argv[-3]
    f2 = sys.argv[-2]
    fo = sys.argv[-1]
    with open(fo, "w") as fileout:
        t1 = ""
        t2 = ""
        with open(f1) as fi:
            t1 = fi.read()
        with open(f2) as fi:
            t2 = fi.read()
        fileout.write(t1)
        fileout.write(t2)
    print("Done~")