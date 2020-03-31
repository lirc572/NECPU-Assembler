#!/usr/bin/env python3
# -*- coding: utf-8 -*-

CPU_FREQ = 25000000

RAM_CODE = '''
`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 03/30/2020 04:22:04 PM
// Design Name: 
// Module Name: RAM
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module RAM(
    input clk,
    input  [15:0] address,
    input  [31:0] data_in,
    output reg [31:0] data_out,
    input  read,
    input  write
    );
    
    reg [31:0] memory [0:65535];
    
    initial begin
        %s
    end
    
    always @ (negedge clk) begin //negedge!!!
        if (read)
            data_out <= memory[address[15:0]];
        else if (write)
            memory[address[15:0]] <= data_in;
    end
    
endmodule
'''

def delayFunc():
    def delayGenerator(sec, freq):
        delayGenerator.number += 1
        delcounter = int(sec * freq / 6)
        return "    LWi $30, %d\nDELAY%d:\n    SUBi $30, $30, 1\n    BEQ $30, 0\n    JUMP DELAY%d\n" % (delcounter, delayGenerator.number, delayGenerator.number)
    delay.number = 0
    return delayGenerator

# Load bitmaps (converted using convert.py):
images = {}
with open("bitmap/start.bitmap") as bmp:
    images["start"] = bmp.readlines()
with open("bitmaps/start_word.bitmap") as bmp:
    images["word"] = bmp.readlines()
with open("bitmaps/start_menu.bitmap") as bmp:
    images["menu"] = bmp.readlines()
with open("bitmaps/map.bitmap") as bmp:
    images["map"] = bmp.readlines()
with open("bitmaps/char.bitmap") as bmp:
    images["char"] = bmp.readlines()
with open("bitmaps/enemy.bitmap") as bmp:
    images["enemy"] = bmp.readlines()
with open("bitmaps/char_gg.bitmap") as bmp:
    images["chargg"] = bmp.readlines()
with open("bitmaps/bo_arrow.bitmap") as bmp:
    images["bo_arrow"] = bmp.readlines()
with open("bitmaps/bo_tail1.bitmap") as bmp:
    images["bo_tail1"] = bmp.readlines()
with open("bitmaps/bo_tail2.bitmap") as bmp:
    images["bo_tail2"] = bmp.readlines()

ram_addr = 0;
img_addrs = {}

ram_data = []

for img in images:
    img_addrs[img] = ram_addr;
    while (len(images[img]) > 1):
        ram_data.append(eval(images[img][1])<<16+eval(img[0])) #RAM: [{img[1], img[0]}, {img[3], img[2]}, ...]
        ram_addr += 1
        images[img] = images[img][2:]
    if len(images[img] == 1):
        ram_data.append(eval(images[img][0]))                  #If odd number of pixels, last memory addr holds one pix at lower half
        ram_addr += 1

RAM_DATA_STR = ""
for dt in ram_data:
    ram_addr = 0
    RAM_DATA_STR += "        memory[%d] <= 16'd%d;\n" % (ram_addr, dt)

# Full verilog code for ram module
RAM_CODE = RAM_CODE % (RAM_DATA_STR,)


DELAY = delayFunc()

# Full NE assembly code of the game
GAMECODE = '''
START:

//display start screen
    LWI  $31, ''' + img_addrs['start'] + ''' //Load starting address of start image      to $31
    ADDi $31, $31, 1                         //Add 1 to skip picture size data
    LWI  $30, 2147500000                     //Load starting address of oled framebuffer to $30
    LWI  $29, 3072                           //Repeats left                              at $29
LOADSTART:
    LW   $28, $31, 0                         //Load pixel data (2pix)                    to $28
    SW   $28, $30, 0                         //Store pixel data to oled framebuffer
    LWI  $27, 16                             //16, the number of bits to shift, loaded   to $27
    SRL  $28, $28, $27                       //Right shift 16 bits to get the next pix
    ADDi $30, $30, 1                         //Shift framebuffer pointer to the next pix
    SW   $28, $30, 0                         //Store pixel data to oled framebuffer
    SUBi $29, $29, 1                         //Number of repeats decreases by 1
    ADDi $31, $31, 1                         //Shift RAM pointer to the next pix
    ADDi $30, $30, 1                         //Shift framebuffer pointer to the next pix
    BEQ  $29, 0
    JUMP LOADSTART

//delay 0.5s
''' + DELAY(0.5, CPU_FREQ) + '''

//display start words
($0 = return_address, $1 = img_mem_addr, $2 = {x_start, y_start}
    LWI  $0, LINE_NUMBER
    LWI  $1, ''' + img_addrs['word'] + '''
    LWI  $2, 720911                          //(11, 15)
    JUMP DISPLAYIMG

//delay 0.5s
''' + DELAY(0.5, CPU_FREQ) + '''

//check if volume is 15, if so move on, else go back to the start
//volume: MEM[2147483650][19:16]
    LWI  $30, 2147483650
    LW   $30, $30, 0
    LWI  $31, 16
    SRL  $30, $30, $31
    ANDi $30, $30, 0b0000000000001111
    BEQ  $30, 15
    JUMP START

//delay 2s
''' + DELAY(2, CPU_FREQ) + '''

//display instructions
    LWI  $0, LINE_NUMBER
    LWI  $1, ''' + img_addrs['menu'] + '''
    LWI  $2, 262150                          //(4, 6)
    JUMP DISPLAYIMG

//check if volume is 15, if so move on, else check again
//volume: MEM[2147483650][19:16]
SHOWINGMENU:
    LWI  $30, 2147483650
    LW   $30, $30, 0
    LWI  $31, 16
    SRL  $30, $30, $31
    ANDi $30, $30, 0b0000000000001111
    BEQ  $30, 15
    JUMP SHOWINGMENU

//load game screen
%s

//load char
%s

//load monsters
%s



//FUNCTIONS:

DISPLAYIMG:
//  parameters: ($0 = return_address, $1 = img_mem_addr, $2 = {x_start, y_start}, $? = pixel_size...) //to-do, currently missing border for odd-pix-lines // not accounting for transparent pixes (16'd0)
//  returns   : (nothing)
//      img_mem_addr points to img size!
//      draw pix by pix until end of img line or end of oled line
//      draw line by line until end of img vert or end of oled vert

    LW   $3,  $1,  0                         //Load img size ({x, y})                    to $3
    ADDi $1,  $1,  1                         //Add 1 to skip picture size data           to $3
    LWI  $4,  2147500000                     //Load starting address of oled framebuffer to $4
    LWI  $20, 16                             //16, the number of bits to shift, loaded   to $20
    SRL  $5,  $2,  $20                       //x_start                                   at $5
    SLL  $6,  $2,  $20                       //y_start                                   at $6
    SRL  $6,  $6,  $20                       //With above
    LWI  $7,  0                              //Numbers to shift, initialized to 0        at $7
DISPMUL0START:
    BEQ  $6,  0                              //Multiplication... ($6 * 96)
    BEQ  $20, 16                             //Skip the next instruction ($20 === 16)
    JUMP DISPMUL0DONE                        //Multiplication done
    ADDi $7,  $7, 96                         //Add 96                                    to $7
    JUMP DISPMUL0START                       //Loop
DISPMUL0DONE:
    ADD  $4,  $4, $7                         //Store fb address of line start            at $4

    SLL  $6,  $3,  $20                       //Vertical Repeats left                     at $6
    SRL  $6,  $6,  $20                       //With above
    SLL  $21, $2,  $20                       //y_coord
    SRL  $21, $21, $20                       //With above
    SRL  $5,  $3,  $20                       //Horizontal Repeats left                   at $5
    ANDi $19, $19, 0                         //clear $19
DISPHOR:                       //new line
    BNE  $21, 64
    JUMP $0                    //last line of oled reached, return
    BNE  $6, 0
    JUMP $0                    //last line of img reached, return
    SRL  $7,  $2,  $20                       //x_coord                                   at $7
    BEQ  $19, 0
    JUMP DISPONEFROMLAST
    JUMP DISPNEXTADR
DISPONEFROMLAST:
    ADD  $8,  $7,  $4                        //fb address                                at $8
    BEQ  $19, 0                              //Test for traansparancy......
    SW   $19, $8,  0                         //Store pixel1 data to oled framebuffer
    ADDi $7,  $7,  1                         //x++                                       to $7
DISPNEXTADR:                   //new pix
    ADD  $8,  $7,  $4                        //fb address                                at $8
    BEQ  $5,  1
    JUMP DISPTWOPIXLEFT
    JUMP DISPONEPIXLEFT
DISPTWOPIXLEFT:
    ANDi $19, $19, 0                         //clear $19
    BNE  $7,  96                             //If not endl, skip next jump
    JUMP DISPENDL
    LW   $9,  $1,   0                        //Load pixel data (2pix)                    to $9
    SLL  $10, $9,  $20                       //1st pixel                                 to $10
    SRL  $10, $10, $20                       //With above
    SRL  $11, $9,  $20                       //2nd pixel                                 to $11
    SUBi $5,  $5,  2                         //Horizontal Repeats left -= 2              to $5
    BEQ  $10, 0                              //Test for traansparancy......
    SW   $10, $8,  0                         //Store pixel1 data to oled framebuffer
    ADDi $7,  $7,  1                         //x++                                       to $7
    BNE  $7,  96                             //If not endl, skip next jump
    JUMP DISPENDL
    BEQ  $11, 0                              //Test for traansparancy......
    SW   $11, $8,  1                         //Store pixel2 data to oled framebuffer
    ADDi $7,  $7,  1                         //x++                                       to $7
    JUMP DISPNEXTADR
DISPONEPIXLEFT:
    ANDi $19, $19, 0                         //clear $19
    BNE  $7,  96                             //If not endl, skip next jump
    JUMP DISPENDL
    LW   $9,  $1,  0                         //Load pixel data (2pix)                    to $9
    SLL  $10, $9,  $20                       //1st pixel                                 to $10
    SRL  $10, $10, $20                       //With above
    BEQ  $10, 0                              //Test for traansparancy......
    SW   $10, $8,  0                         //Store pixel1 data to oled framebuffer
    ADDi $7,  $7,  1                         //x++                                       to $7
    BNE  $7,  96                             //If not endl, skip next jump
    JUMP DISPENDL
    SRL  $11, $9,  $20                       //2nd pixel                                 to $11
    ANDi $19, $11, 0x0000FFFF                //load 2nd pixel                            to $19
DISPENDL:
    ADDi $4,  $4,  96                        //fb pointer to next line start
    SUBi $6,  $6,  1
    ADDi $21, $21, 1
    JUMP DISPHOR


'''