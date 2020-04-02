#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import NEFunctions as Functions

'''
Note:
    LINE_NUMBER+5 because LWI takes two real instructions and JUMP takes 3 real instructions...
'''

# Full NE assembly code of the game
GAMECODE =  "START:\n"
GAMECODE += "    LWI  $0, LINE_NUMBER+5\n"
GAMECODE += "    JUMP DISPSTART\n"
GAMECODE += Functions.delayGenerator(0.5, "DELAYSTART")
GAMECODE += "    LWI  $0, LINE_NUMBER+5\n"
GAMECODE += "    JUMP DISPWORD\n"
GAMECODE += Functions.delayGenerator(0.5, "DELAYWORD")
GAMECODE += "    LWI  $0, 0\n"
GAMECODE += "    LWI  $1, LINE_NUMBER+5\n"
GAMECODE += "    JUMP CHECKVOLUME\n"
GAMECODE += "    LWI  $0, LINE_NUMBER+5\n"
GAMECODE += "    JUMP DISPMENU\n"
GAMECODE += Functions.delayGenerator(2, "DELAYMENU")
GAMECODE += "    LWI  $0, LINE_NUMBER\n"
GAMECODE += "    LWI  $1, LINE_NUMBER+5\n"
GAMECODE += "    JUMP CHECKVOLUME\n"
GAMECODE += "    LWI  $1, 12\n"            #centre_x of map: 12
GAMECODE += "    LWI  $2, 9\n"             #centre_x of map: 9
GAMECODE += "    LWI  $0, LINE_NUMBER+5\n"
GAMECODE += "    JUMP DISPMAP\n"
GAMECODE += "    LWI  $1, 0\n"
GAMECODE += "    LWI  $0, LINE_NUMBER+5\n"
GAMECODE += "    JUMP DISPCHAR\n"
GAMECODE += "    JUMP BLINK\n"
GAMECODE += Functions.BLINK
GAMECODE += Functions.DISPSTART
GAMECODE += Functions.DISPWORD
GAMECODE += Functions.DISPMENU
GAMECODE += Functions.DISPCHAR
GAMECODE += Functions.CHECKVOLUME
GAMECODE += Functions.DISPMAP
GAMECODE += Functions.GETMAPCOLOR

with open("Game.asm", "w") as src:
    src.write(GAMECODE)
print("Game.asm generated!")
