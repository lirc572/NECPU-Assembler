#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import NEFunctions as Functions

# Full NE assembly code of the game
GAMECODE =  "START:\n"
GAMECODE += "    LWI  $0, LINE_NUMBER+2\n"
GAMECODE += "    JUMP DISPWORD\n"
GAMECODE += Functions.delayGenerator(0.5, "DELAYWORD")
GAMECODE += "    LWI  $0, 0\n"
GAMECODE += "    LWI  $1, LINE_NUMBER+2\n"
GAMECODE += "    JUMP CHECKVOLUME\n"
GAMECODE += "    LWI  $0, LINE_NUMBER+2\n"
GAMECODE += "    JUMP DISPMENU\n"
GAMECODE += Functions.delayGenerator(2, "DELAYMENU")
GAMECODE += "    LWI  $0, LINE_NUMBER\n"
GAMECODE += "    LWI  $1, LINE_NUMBER+2\n"
GAMECODE += "    JUMP CHECKVOLUME\n"
GAMECODE += "    LWI  $1, 0\n"
GAMECODE += "    LWI  $0, LINE_NUMBER+2\n"
GAMECODE += "    JUMP DISPCHAR\n"
GAMECODE += "    JUMP BLINK\n"
GAMECODE += Functions.BLINK
GAMECODE += Functions.DISPSTART
GAMECODE += Functions.DISPWORD
GAMECODE += Functions.DISPMENU
GAMECODE += Functions.DISPCHAR
GAMECODE += Functions.CHECKVOLUME

with open("GT.asm", "w") as src:
    src.write(GAMECODE)
print("GT.asm generated!")