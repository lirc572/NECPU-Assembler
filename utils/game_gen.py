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

#Game Loop initialization... Set game level (global) variables that *must not* be used by any function in the loop!
gamecode.append("    LWI  $29, 0")                #$29: character state
gamecode.append("    LWI  $27, 0")                #$27: chara x
gamecode.append("    LWI  $28, 0")                #$28: chara y
gamecode.append("GAMELOOP:")

#Ending condition test...
gamecode.append("    LWI  $20, 69")    #door x
gamecode.append("    LWI  $21, 43")    #door y
gamecode.append("    SLT  $25, $20, $27")
gamecode.append("    SLT  $26, $21, $28")
gamecode.append("    BEQ  $25, 1")        #if met, skip
gamecode.append("    JUMP CONTROLHANDLE")
gamecode.append("    BEQ  $26, 1")        #if met, skip
gamecode.append("    JUMP CONTROLHANDLE")
gamecode.append("    JUMP GAMEOVER")

#Control handling...
gamecode.append("CONTROLHANDLE:")
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
gamecode.append("    JUMP CONTROLDEF")            #default: goto CONTROLDEF
gamecode.append("BTNDPRESSED:")
gamecode.append("    SUBi $28, $28, 1")           #move down
gamecode.append("    LWI  $29, 0")                #set state: gg
gamecode.append("    LLI  $5,  1")
gamecode.append("    LWI  $6,  2147483648")
gamecode.append("    SW   $5,  $6, 0")
gamecode.append("    JUMP CONTROLEND")
gamecode.append("BTNRPRESSED:")
gamecode.append("    ADDi $27, $27, 1")           #move right
gamecode.append("    LWI  $29, 3")                #set state: r1
gamecode.append("    LLI  $5,  2")
gamecode.append("    LWI  $6,  2147483648")
gamecode.append("    SW   $5,  $6, 0")
gamecode.append("    JUMP CONTROLEND")
gamecode.append("BTNLPRESSED:")
gamecode.append("    SUBi $27, $27, 1")           #move left
gamecode.append("    LWI  $29, 1")                #set state: l1
gamecode.append("    LLI  $5,  4")
gamecode.append("    LWI  $6,  2147483648")
gamecode.append("    SW   $5,  $6, 0")
gamecode.append("    JUMP CONTROLEND")
gamecode.append("BTNUPRESSED:")
gamecode.append("    ADDi $28, $28, 1")           #move up
gamecode.append("    LWI  $29, 5")                #set state: back
gamecode.append("    LLI  $5,  8")
gamecode.append("    LWI  $6,  2147483648")
gamecode.append("    SW   $5,  $6, 0")
gamecode.append("    JUMP CONTROLEND")
gamecode.append("CONTROLDEF:")
gamecode.append("    LLI  $5,  16")
gamecode.append("    LWI  $6,  2147483648")
gamecode.append("    SW   $5,  $6, 0")
gamecode.append("CONTROLEND:")

#Display Map...
gamecode.append("    LWI  $0,  LINE_NUMBER+5")    #set return addr
gamecode.append("    JUMP DISPSIMPLEMAP")               #function call

#Display character...
gamecode.append("    ADDi $1,  $29, 0")           #ccopy char_state to $1
gamecode.append("    ADDi $2,  $27, 0")           #x
gamecode.append("    ADDi $3,  $28, 0")           #y
gamecode.append("    LWI  $0,  LINE_NUMBER+5")    #set return addr
gamecode.append("    JUMP DISPCHARA")             #function call

gamecode.append(Functions.delayGenerator(0.01, "DELAYPOV"))

#Goto GAMELOOP...
gamecode.append("    JUMP GAMELOOP")

gamecode.append("GAMEOVER:")

#Endless blinky to indicate end of program execution...
gamecode.append("    JUMP BLINK")

#Load function definitions...
gamecode.append(Functions.DISPSTART)
gamecode.append(Functions.DISPWORD)
gamecode.append(Functions.DISPCHARA)
gamecode.append(Functions.CHECKVOLUME)
gamecode.append(Functions.DISPSIMPLEMAP)
gamecode.append(Functions.DIVISION)
gamecode.append(Functions.MODULUS)
gamecode.append(Functions.MULTIPLICATION)
gamecode.append(Functions.BLINK)

with open("Game.asm", "w") as src:
    src.write('\n'.join(filter(lambda x: x, gamecode.toString().split('\n')))) #remove empty lines
print("Game.asm generated!")
