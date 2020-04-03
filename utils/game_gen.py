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

#Start Scene...
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

#Game Loop initialization... Set game level (global) variables that *must not* be used by any function in the loop!
gamecode.append("    LWI  $30, 12*16")            #$30: centre_x of map: 12*16
gamecode.append("    LWI  $31, 9*16 ")            #$31: centre_y of map: 9*16
gamecode.append("    LWI  $29, 0")                #$29: character state
gamecode.append("    LWI  $27, 12*16+10")         #$27: enemy_x
gamecode.append("    LWI  $28, 9*16-10")          #$28: enemy_y
gamecode.append("GAMELOOP:")

#Control handling...
gamecode.append("    LWI  $1,  2147483649")       #load addr of btns to $1
gamecode.append("    LW   $1,  $1, 0")            #load btn data into $1
gamecode.append("    LWI  $2,  27")               #bits to shift
gamecode.append("    SLL  $1,  $1,  $2")          #shift left to remove x's
gamecode.append("    SRL  $1,  $1,  $2")          #shift right to move back in position
gamecode.append("    BNE  $1,  0b10000")          #if btnD
gamecode.append("    JUMP BTNDPRESSED")
gamecode.append("    BNE  $1,  0b01000")          #if btnR
gamecode.append("    JUMP BTNRPRESSED")
gamecode.append("    BNE  $1,  0b00100")          #if btnL
gamecode.append("    JUMP BTNLPRESSED")
gamecode.append("    BNE  $1,  0b00010")          #if btnU
gamecode.append("    JUMP BTNUPRESSED")
gamecode.append("    JUMP CONTROLEND")            #default: goto CONTROLDEF
gamecode.append("BTNDPRESSED:")
gamecode.append("    SUBi $31, $31, 1")           #move down
gamecode.append("    LWI  $29, 0")                #set state: gg
gamecode.append("    JUMP CONTROLEND")
gamecode.append("BTNRPRESSED:")
gamecode.append("    ADDi $30, $30, 1")           #move right
gamecode.append("    LWI  $29, 3")                #set state: r1
gamecode.append("    JUMP CONTROLEND")
gamecode.append("BTNLPRESSED:")
gamecode.append("    SUBi $30, $30, 1")           #move left
gamecode.append("    LWI  $29, 1")                #set state: l1
gamecode.append("    JUMP CONTROLEND")
gamecode.append("BTNUPRESSED:")
gamecode.append("    ADDi $31, $31, 1")           #move up
gamecode.append("    LWI  $29, 0")                #set state: gg
gamecode.append("    JUMP CONTROLEND")
gamecode.append("CONTROLDEF:")
gamecode.append("CONTROLEND:")

#Display Map...
gamecode.append("    ADDi $1,  $30, 0")           #copy centre_x to $1
gamecode.append("    ADDi $2,  $31, 0")           #copy centre_y to $2
gamecode.append("    LWI  $0,  LINE_NUMBER+5")    #set return addr
gamecode.append("    JUMP DISPMAP")               #function call

#Display Enemy...
#  Use map centre data from last few lines so dun change $1 and $2!!!
gamecode.append("    ADDi $3,  $27, 0")           #copy enemy_x to $3
gamecode.append("    ADDi $4,  $28, 0")           #copy enemy_y to $4
gamecode.append("    LWI  $0,  LINE_NUMBER+5")    #set return addr
gamecode.append("    JUMP DISPENEMY")             #function call

#Display character...
gamecode.append("    ADDi $1,  $29, 0")           #ccopy char_state to $1
gamecode.append("    LWI  $0,  LINE_NUMBER+5")    #set return addr
gamecode.append("    JUMP DISPCHAR")              #function call

gamecode.append(Functions.delayGenerator(0.01, "DELAYPOV"))

#Goto GAMELOOP...
gamecode.append("    JUMP GAMELOOP")

#Endless blinky to indicate end of program execution...
gamecode.append("    JUMP BLINK")

#Load function definitions...
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
    src.write('\n'.join(filter(lambda x: x, gamecode.toString().split('\n')))) #remove empty lines
print("Game.asm generated!")
