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

def appendFunction(code, function, debug = False):
        return code + function

gamecode = GameCode()

'''
Note:
    LINE_NUMBER+5 because LWI takes two real instructions and JUMP takes 3 real instructions...
'''

# Full NE assembly code of the game

gamecode.append("START:")
gamecode.append("    LWI  $0, LINE_NUMBER+5")
gamecode.append("    JUMP DISPSTART")
gamecode.append(Functions.delayGenerator(0.5, "DELAYSTART"))
gamecode.append("    LWI  $0, LINE_NUMBER+5")
gamecode.append("    JUMP DISPWORD")
gamecode.append(Functions.delayGenerator(0.5, "DELAYWORD"))
gamecode.append("    LWI  $0, 0")
gamecode.append("    LWI  $1, LINE_NUMBER+5")
gamecode.append("    JUMP CHECKVOLUME")
gamecode.append("    LWI  $0, LINE_NUMBER+5")
gamecode.append("    JUMP DISPMENU")
gamecode.append(Functions.delayGenerator(2, "DELAYMENU"))
gamecode.append("    LWI  $0, LINE_NUMBER")
gamecode.append("    LWI  $1, LINE_NUMBER+5")
gamecode.append("    JUMP CHECKVOLUME")
#gamecode.append("    LWI  $1, 12")            #centre_x of map: 12
#gamecode.append("    LWI  $2, 9 ")            #centre_x of map: 9
#gamecode.append("    LWI  $0, LINE_NUMBER+5")
#gamecode.append("    JUMP DISPMAP")
#gamecode.append("    LWI  $3, 12")
#gamecode.append("    LWI  $4, 9")
#gamecode.append("    LWI  $0, LINE_NUMBER+5")
#gamecode.append("    JUMP DISPENEMY")
#gamecode.append("    LWI  $1, 0")
#gamecode.append("    LWI  $0, LINE_NUMBER+5")
#gamecode.append("    JUMP DISPCHAR")
gamecode.append("    JUMP BLINK")

gamecode.append(Functions.DISPSTART)
gamecode.append(Functions.DISPWORD)
gamecode.append(Functions.DISPMENU)
gamecode.append(Functions.DISPCHAR)
gamecode.append(Functions.DISPENEMY)
gamecode.append(Functions.CHECKVOLUME)
gamecode.append(Functions.DISPMAP)
gamecode.append(Functions.GETMAPCOLOR)
gamecode.append(Functions.DIVISION)
gamecode.append(Functions.MODULUS)
gamecode.append(Functions.MULTIPLICATION)
gamecode.append(Functions.BLINK)

with open("Game.asm", "w") as src:
    src.write(gamecode.toString())
print("Game.asm generated!")
