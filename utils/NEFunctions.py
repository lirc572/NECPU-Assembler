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
#   DISPMAP     ($0: return_addr, $1: centre_x, $2: centre_y)
#   GETMAPCOLOR ($3: x_coord, $4: y_coord, $5: return_addr)
#       return: ($6: color)
#   DISPENEMY   ($0: return_addr, $1: centre_x, $2: centre_y, $3: enemy_x_rel_map, $4: enemy_y_rel_map)
#   DIVISION    ($9: return_addr, $10: A, $11: B)
#       return: ($12: C)
#   MODULUS     ($9: return_addr, $10: A, $11: B)
#       return  ($12: C)
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

DISPWORD = "DISPWORD:\n"
WORDX = int(images["word"][0])
WORDY = int(images["word"][1])
WORDSTARTX = (OLEDX-WORDX)//2
WORDSTARTY = (OLEDY-WORDY)//2
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

DISPMENU = "DISPMENU:\n"
MENUX = int(images["menu"][0])
MENUY = int(images["menu"][1])
MENUSTARTX = (OLEDX-MENUX)//2
MENUSTARTY = (OLEDY-MENUY)//2
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
DISPCHAR = "DISPCHAR:\n"
CHARX = int(images["chargg"][0])
CHARY = int(images["chargg"][1])
CHARSTARTX = (OLEDX-CHARX)//2
CHARSTARTY = (OLEDY-CHARY)//2
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

#centre_x: $1, centre_y: $2
DISPMAP = "DISPMAP:\n"
MAPSCALEEXP = 4 # coord>>4
MAPX = int(images["map"][0])
MAPY = int(images["map"][1])
DISPMAP += "    LWI  $10, 0\n"                    #$10 = oled addr
inst  = "DISPMAPLOOP:\n"
inst += "    LWI  $11, %d\n" % (OLEDX,)           #$11 = OLEDX
inst += "    LWI  $9,  LINE_NUMBER+5\n"           #Return addr
inst += "    JUMP MODULUS\n"                      #$12 = $10 % $11
inst += "    ADDi $15, $12, 0\n"                  #$15 = result
inst += "    LWI  $16, 1\n"                       #$16 = 1
inst += "    SRL  $16, $11, $16\n"                #$16 = OLEDX >> 1
inst += "    SUB  $15, $15, $16\n"                #x_offset
inst += "    LWI  $9,  LINE_NUMBER+5\n"           #Return addr
inst += "    JUMP DIVISION\n"                     #$12 = $10 / $11
inst += "    ADDi $16, $12, 0\n"                  #$16 = result
inst += "    LWI  $17, %d\n" % (OLEDY,)           #$17 = OLEDY
inst += "    LWI  $18, 1\n"                       #$18 = 1
inst += "    SRL  $17, $17, $18\n"                #$17 = OLEDY >> 1
inst += "    SUB  $16, $16, $17\n"                #y_offset
inst += "    ADDi $10, $10, 1\n"                  #$10 ++; increment addr
inst += "    ADD  $3,  $1,  $15\n"                #$3 = x coord on big map
inst += "    ADD  $4,  $2,  $16\n"                #$4 = y_coord on big map
inst += "    LWI  $5,  %d\n" % (MAPSCALEEXP,)     #scale factor as power of 2
inst += "    SRL  $3,  $3,  $5\n"                 #$3 = x_coord on small map
inst += "    SRL  $4,  $4,  $5\n"                 #$4 = y_coord on small map
inst += "    LWI  $5,  LINE_NUMBER+5\n"           #return_addr for GETMAPCOLOR
inst += "    JUMP GETMAPCOLOR\n"                    #$6 = color
inst += "    LWI  $5,  %d\n" % (2147500000+addr,) #pix addr in memory
inst += "    SW   $6,  $5,  0\n"                  #Draw pixel
inst += "    BEQ  $10, %d\n" % (OLEDX*OLEDY,)     #If end of oled reached, skip next line
inst += "    JUMP DISPMAPLOOP\n"                  #GOTO DISPMAPLOOP
inst += "    JMP  $0\n"                           #Return...
DISPMAP += inst

#x_cooord: $3, y_coord: $4
#return addr: $5
GETMAPCOLOR = "GETMAPCOLOR:\n"
imgaddr = -1
for i in range(MAPX):
    inst  = "    BNE  $3, %d\n" % (i,)
    inst += "    JUMP MAPX%d\n" % (i,)
    GETMAPCOLOR += inst
GETMAPCOLOR += "    LWI  $6, 0\n    JMP  $5\n" #Return black if x out of range
for i in range(MAPX):
    inst  = "MAPX%d:\n" % (i,)
    for j in range(MAPY):
        inst += "    BNE  $4, %d\n" % (j,)
        inst += "    LWI  $6, %s" % (images["map"][2+j*MAPX+i],)
    inst += "    JMP  $5\n"
    GETMAPCOLOR += inst
del MAPX
del MAPY
del MAPSCALEEXP

#centre_x: $1, centre_y: $2
#enemy_x:  $3, enemy_y:  $4
DISPENEMY = "DISPENEMY:\n"
ENEMYX = int(images["enemy"][0])
ENEMYY = int(images["enemy"][1])
ENEMY = {}
addr = -1
for pix in images["enemy"][2:]:
    addr += 1
    if eval(pix) != 0:
        if pix in ENEMY:
            ENEMY[pix].append(addr)
        else:
            ENEMY[pix] = [addr]
DISPENEMY += "    LWI  $13, 1\n"                         #$13 = constant 1
DISPENEMY += "    LWI  $14, %d\n" % (OLEDX,)             #$14 = OLEDX
DISPENEMY += "    LWI  $15, %d\n" % (OLEDY,)             #$15 = OLEDY
for i in ENEMY:
    inst = "    LLI  $16, %s" % (i,)                     #$16 = color
    for j in ENEMY[i]:
        inst += "    SRL  $5,  $14, $13\n"               #$5 = OLEDX >> 1
        inst += "    SUB  $6,  $3,  $1 \n"               #$6 = EX - CX
        inst += "    ADD  $5,  $6,  $5 \n"               #$5 = $6 + $5 (EXscr)
        inst += "    SRL  $6,  $15, $13\n"               #$6 = OLEDY >> 1
        inst += "    SUB  $7,  $4,  $2 \n"               #$7 = EY - CY
        inst += "    ADD  $6,  $7,  $6 \n"               #$6 = $7 + $6 (EYscr)
        inst += "    ADDi $5,  $5,  %d\n" % (j% ENEMYX,) #$5 = Pix_x
        inst += "    ADDi $6,  $6,  %d\n" % (j//ENEMYX,) #$6 = Pix_y
        inst += "    SLT  $7,  $5,  $14\n"               #$7 = Pix_x < OLEDX
        inst += "    SLT  $8,  $6,  $15\n"               #$8 = Pix_y < OLEDY
        inst += "    BEQ  $7,  1\n"                      #if within boundary, skip next
        inst += "    JUMP %s\n" % ("DISPENEMY%s%sEND" % (i[:-1], j,),)
        inst += "    BEQ  $8,  1\n"                      #if within boundary, skip next
        inst += "    JUMP %s\n" % ("DISPENEMY%s%sEND" % (i[:-1], j,),)
        inst += "    ADDi $10, $6, 0\n"                  #$10 = Pix_y
        inst += "    LWI  $11, %d\n" % (ENEMYX,)         #$11 = ENEMYX
        inst += "    LWI  $9,  LINE_NUMBER+5\n"          #$9 = Return addr
        inst += "    JUMP MULTIPLICATION\n"              #$12 = $10 * $11
        inst += "    ADD  $12, $12, $5\n"                #$12 = Pix_addr
        inst += "    SW   $16, $12\n"                    #Draw $16 at $12
        inst += "DISPENEMY%s%sEND:\n" % (i[:-1], j,)
    DISPENEMY += inst
DISPENEMY += "    JMP $0\n"
del ENEMY
del ENEMYX
del ENEMYY


DISPBO = "DISPBO:\n"



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

#a//b = c
#return_addr: $9
#a: $10, b: $11, c: $12
DIVISION = '''
DIVISION:
    LWI  $12, 0
    LWI  $13, 0
DIVISIONLOOP:
    ADD  $13, $13, $11
    SLT  $14, $10, $13
    BNE  $14, 1
    JMP  $9
    ADDi $12, $12, 1
    JUMP DIVISIONLOOP
'''

#a%b = c
#return_addr: $9
#a: $10, b: $11, c: $12
MODULUS = '''
MODULUS:
    LWI  $12, 0
MODULUSLOOP:
    ADD  $12, $12, $11
    SLT  $13, $10, $12
    BNE  $13, 1
    JUMP MODULUSFIN
    JUMP MODULUSLOOP
MODULUSFIN:
    SUB  $12, $12, $11
    SUB  $12, $10, $12
    JMP  $9
'''

#a*b = c
#return_addr: $9
#a: $10, b: $11, c: $12
MULTIPLICATION = '''
MULTIPLICATION:
    LWI  $12, 0
    ADDi $13, $11, 0
MULTIPLICATIONLOOP:
    SUBi $13, $13, 1
    ADD  $12, $12, $10
    BNE  $13, 0
    JMP  $9
    JUMP  MULTIPLICATIONLOOP
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
