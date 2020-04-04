#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import NEFunctions as Functions

class GameCode:
    def __init__(self):
        self.Code = ""
    def append(self, code):
        self.Code += code
        if code[-1] != '\n':
            self.Code += '\n'
    def toString(self):
        return self.Code


gamecode = GameCode()

#Display Map...
gamecode.append("    LWI  $30, 12*16")            #$30: centre_x of map: 12*16
gamecode.append("    LWI  $31, 9*16 ")            #$31: centre_y of map: 9*16
gamecode.append("    ADDi $1,  $30, 0")           #copy centre_x to $1
gamecode.append("    ADDi $2,  $31, 0")           #copy centre_y to $2
gamecode.append("    LWI  $0,  LINE_NUMBER+5")    #set return addr
gamecode.append("    JUMP DISPMAP")               #function call
gamecode.append("    JUMP BLINK")
gamecode.append(Functions.DISPMAP)
gamecode.append(Functions.GETMAPCOLOR)
gamecode.append(Functions.BLINK)
gamecode.append(Functions.MODULUS)
gamecode.append(Functions.DIVISION)
gamecode.append(Functions.MULTIPLICATION)


with open("GT.asm", "w") as src:
    src.write('\n'.join(filter(lambda x: x, gamecode.toString().split('\n')))) #remove empty lines
print("GT.asm generated!")