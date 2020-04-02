#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PIL import Image
import sys

size = 0
sequence_of_pixels = []
sequence_of_pixels_16b = []

def rgb16b(fmt, rgb):
    if fmt == 'PNG':
        if rgb[3] == 0:
            return '0'
    r = bin(rgb[0] // 8)[2:]
    g = bin(rgb[1] // 4)[2:]
    b = bin(rgb[2] // 8)[2:]
    r = "0"*(5-len(r)) + r
    g = "0"*(6-len(g)) + g
    b = "0"*(5-len(b)) + b
    if len(r+b+g)>16:
        print(r, g, b)
    return "0b" + ("0" * (16-len(r+g+b))) + (r + g + b)

if __name__ == '__main__':
    img = Image.open(sys.argv[-2])
    fmt = img.format
    assert fmt in ('JPEG', 'PNG')
    size = img.size
    print("Size:", size)
    print("Format:", fmt)
    for j in range(size[1]):
        for i in range(size[0]):
            sequence_of_pixels.append(img.getpixel((i, j)))
    for i in sequence_of_pixels:
        sequence_of_pixels_16b.append(rgb16b(fmt, i))
    with open(sys.argv[-1], "w") as f:
        f.write(str(size[0]) + '\n')
        f.write(str(size[1]) + '\n')
        for i in sequence_of_pixels_16b:
            f.write(i + "\n")
