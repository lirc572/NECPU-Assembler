#!/usr/bin/env python3
# -*- coding: utf-8 -*-
ABOUT = '''
# This file contains all the needed NE assembly functions:
#   DISPSTART   ($0: return_addr)
#   DISPWORD    ($0: return_addr)
#   DISPMENU    ($0: return_addr)
#   DISPCHAR    ($0: return_addr, $1: state)
#   CHECKVOLUME ($0: inst_addr if volume != 15, $1: inst_addr if volume == 15)
#   BLINK       (infinite loop, no input)
'''

CPU_FREQ = 100000000

def delayGenerator(sec, label):
    delcounter = int(sec * CPU_FREQ / 6)
    return "    LWi  $30, %d\n%s:\n    SUBi $30, $30, 1\n    BEQ  $30, 0\n    JUMP %s\n" % (delcounter, label, label)

OLEDX = 96
OLEDY = 64

# Load bitmaps (converted using convert.py):
images = {}
with open("../bitmaps/start.bitmap") as bmp:
    images["start"] = bmp.readlines()
with open("../bitmaps/start_word.bitmap") as bmp:
    images["word"] = bmp.readlines()
with open("../bitmaps/start_menu.bitmap") as bmp:
    images["menu"] = bmp.readlines()
with open("../bitmaps/map.bitmap") as bmp:
    images["map"] = bmp.readlines()
with open("../bitmaps/char.bitmap") as bmp:
    images["char"] = bmp.readlines()
with open("../bitmaps/enemy.bitmap") as bmp:
    images["enemy"] = bmp.readlines()
with open("../bitmaps/char_gg.bitmap") as bmp:
    images["chargg"] = bmp.readlines()
with open("../bitmaps/bo_arrow.bitmap") as bmp:
    images["bo_arrow"] = bmp.readlines()
with open("../bitmaps/bo_tail1.bitmap") as bmp:
    images["bo_tail1"] = bmp.readlines()
with open("../bitmaps/bo_tail2.bitmap") as bmp:
    images["bo_tail2"] = bmp.readlines()

DISPSTART = "DISPSTART:\n"
START = {}
addr = -1
for pix in images["start"][2:]:
    addr += 1
    if pix in START:
        START[pix].append(addr)
    else:
        START[pix] = [addr]
for i in START:
    inst = "    LLI  $1, %s" % (i,)
    for j in START[i]:
        inst += "    LWI  $2, %d\n" % (2147500000+j,)
        inst += "    SW   $1, $2, 0\n"
    DISPSTART += inst
DISPSTART += "    JMP $0\n"
del START

WORDX = int(images["word"][0])
WORDY = int(images["word"][1])
WORDSTARTX = (OLEDX-WORDX)//2
WORDSTARTY = (OLEDY-WORDY)//2
DISPWORD = "DISPWORD:\n"
WORD = {}
addr = -1
for pix in images["word"][2:]:
    addr += 1
    if eval(pix) != 0:
        if pix in WORD:
            WORD[pix].append(addr)
        else:
            WORD[pix] = [addr]
for i in WORD:
    inst = "    LLI  $1, %s" % (i,)
    for j in WORD[i]:
        inst += "    LWI  $2, %d\n" % ((2147500000+WORDSTARTY*OLEDX+WORDSTARTX) + j//WORDX*OLEDX+j%WORDX,)
        inst += "    SW   $1, $2, 0\n"
    DISPWORD += inst
DISPWORD += "    JMP $0\n"
del WORD
del WORDSTARTX
del WORDSTARTY
del WORDX
del WORDY

MENUX = int(images["menu"][0])
MENUY = int(images["menu"][1])
MENUSTARTX = (OLEDX-MENUX)//2
MENUSTARTY = (OLEDY-MENUY)//2
DISPMENU = "DISPMENU:\n"
MENU = {}
addr = -1
for pix in images["menu"][2:]:
    addr += 1
    if eval(pix) != 0:
        if pix in MENU:
            MENU[pix].append(addr)
        else:
            MENU[pix] = [addr]
for i in MENU:
    inst = "    LLI  $1, %s" % (i,)
    for j in MENU[i]:
        inst += "    LWI  $2, %d\n" % ((2147500000+MENUSTARTY*OLEDX+MENUSTARTX) + j//MENUX*OLEDX+j%MENUX,)
        inst += "    SW   $1, $2, 0\n"
    DISPMENU += inst
DISPMENU += "    JMP $0\n"
del MENU
del MENUSTARTX
del MENUSTARTY
del MENUX
del MENUY

#state: $1
CHARX = int(images["char"][0])
CHARY = int(images["char"][1])
CHARSTARTX = (OLEDX-CHARX)//2
CHARSTARTY = (OLEDY-CHARY)//2
DISPCHAR = "DISPCHAR:\n"
CHAR = {}
addr = -1
for pix in images["char"][2:]:
    addr += 1
    if eval(pix) != 0:
        if pix in CHAR:
            CHAR[pix].append(addr)
        else:
            CHAR[pix] = [addr]
CHARGG = {}
addr = -1
for pix in images["chargg"][2:]:
    addr += 1
    if eval(pix) != 0:
        if pix in CHARGG:
            CHARGG[pix].append(addr)
        else:
            CHARGG[pix] = [addr]
DISPCHAR += "    BNE  $1, 0\n"
DISPCHAR += "    JUMP CHARGG\n"
DISPCHAR += "    BNE  $1, 1\n"
DISPCHAR += "    JUMP CHARLEFT\n"
DISPCHAR += "    BNE  $1, 2\n"
DISPCHAR += "    JUMP CHARLEFT\n"
DISPCHAR += "    BNE  $1, 3\n"
DISPCHAR += "    JUMP CHARRIGHT\n"
DISPCHAR += "    BNE  $1, 4\n"
DISPCHAR += "    JUMP CHARRIGHT\n"
DISPCHAR += "    JUMP CHARGG\n"
DISPCHAR += "CHARGG:\n"
for i in CHARGG:
    inst = "    LLI  $3, %s" % (i,)
    for j in CHARGG[i]:
        inst += "    LWI  $2, %d\n" % ((2147500000+CHARSTARTY*OLEDX+CHARSTARTX) + j//CHARX*OLEDX+j%CHARX,)
        inst += "    SW   $3, $2, 0\n"
    DISPCHAR += inst
DISPCHAR += "    JUMP CHARAFTERDEF\n"
DISPCHAR += "CHARRIGHT:\n"
for i in CHAR:
    inst = "    LLI  $3, %s" % (i,)
    for j in CHAR[i]:
        inst += "    LWI  $2, %d\n" % ((2147500000+CHARSTARTY*OLEDX+CHARSTARTX) + j//CHARX*OLEDX+j%CHARX,)
        inst += "    SW   $3, $2, 0\n"
    DISPCHAR += inst
DISPCHAR += "    BNE  $1, 3\n"
DISPCHAR += "    JUMP CHARRIGHT1\n"
DISPCHAR += "CHARRIGHT2:\n"
DISPCHAR += ""                                                         ###################################
DISPCHAR += "    JUMP CHARAFTERDEF\n"
DISPCHAR += "CHARRIGHT1:\n"
DISPCHAR += ""                                                         ###################################
DISPCHAR += "    JUMP CHARAFTERDEF\n"
DISPCHAR += "CHARLEFT:\n"
for i in CHAR:
    inst = "    LLI  $3, %s" % (i,)
    for j in CHAR[i]:
        inst += "    LWI  $2, %d\n" % ((2147500000+CHARSTARTY*OLEDX+CHARSTARTX) + (j//CHARX+1)*OLEDX-j%CHARX,)
        inst += "    SW   $3, $2, 0\n"
    DISPCHAR += inst
DISPCHAR += "    BNE  $1, 1\n"
DISPCHAR += "    JUMP CHARLEFT1\n"
DISPCHAR += "CHARLEFT2:\n"
DISPCHAR += ""                                                         ###################################
DISPCHAR += "    JUMP CHARAFTERDEF\n"
DISPCHAR += "CHARLEFT1:\n"
DISPCHAR += ""                                                         ###################################
DISPCHAR += "    JUMP CHARAFTERDEF\n"
DISPCHAR += "CHARAFTERDEF:\n"
DISPCHAR += "    JMP  $0\n" #return
del CHAR
del CHARX
del CHARY

DISPENEMY = "DISPENEMY:\n"

DISPBO = "DISPBO:\n"

DISPMAP = "DISPMAP:\n"


BLINK = '''
BLINK:
    LWI  $3, 2147483648
    LWI  $1, 0b1010101010101010
BLINKLOOP:
    INV  $1, $1
    SW   $1, $3, 0
    LWI  $2, %d
BLINKDEL:
    SUBI $2, $2, 1
    BEQ  $2, 0
    JUMP BLINKDEL
    JUMP BLINKLOOP
''' % (int(1 * CPU_FREQ / 6),)


CHECKVOLUME = '''
//check if volume is 15, if so goto $1, else goto $0
//volume: MEM[2147483650][19:16]
CHECKVOLUME:
    LWI  $2, 2147483650
    LW   $2, $2, 0
    LWI  $3, 16
    SRL  $2, $2, $3
    ANDi $2, $2, 0b0000000000001111
    BEQ  $2, 15
    JMP  $0
    JMP  $1
'''

del i
del j
del inst
del images

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 1:
        print(ABOUT)
        print(eval(input()))
    else:
        print(eval(' '.join(sys.argv[1:])))
