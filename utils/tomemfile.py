#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PIL import Image
import sys

size = 0
sequence_of_pixels = []
sequence_of_pixels_16h = []

CODE1 = '''
`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 03/24/2020 04:29:32 PM
// Design Name: 
// Module Name: OLed_Volume_Display
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

`define CTDefaultVolumeBarL { 5'd0, ~6'd0, 5'd0}
`define CTDefaultVolumeBarM {~5'd0, ~6'd0, 5'd0}
`define CTDefaultVolumeBarH {~5'd0,  6'd0, 5'd0}
`define CTDefaultBackground 16'd0
`define CTDefaultBorder     ~16'd0

`define CTLugeVolumeBarL    { 5'd5, 6'd50, 5'd0 }
`define CTLugeVolumeBarM    {5'd28, 6'd31, 5'd0 }
`define CTLugeVolumeBarH    {5'd30, 6'd0 , 5'd6 }
`define CTLugeBackground    { 5'd1, 6'd5 , 5'd14}
`define CTLugeBorder        { 5'd0, 6'd63, 5'd22}

`define CTRochorVolumeBarL  {5'd0, 6'd33, 5'd5} //(89,97,110)
`define CTRochorVolumeBarM  {5'd12, 6'd22, 5'd14} //(103,89,117)
`define CTRochorVolumeBarH  {5'd10, 6'd27, 5'd13} //(84,111,110)
`define CTRochorBackground  16'd103               //103
`define CTRochorBorder      16'd9825              //\u9825

`define CTLXVolumeBarL    { 5'd0, 6'd32, 5'd3 } //(7,132,22)
`define CTLXVolumeBarM    {5'd6, 6'd46, 5'd8 } //(48,184,64)
`define CTLXVolumeBarH    {5'd14, 6'd59 , 5'd16 } //(112,234,126)
`define CTLXBackground    { 5'd29, 6'd55 , 5'd22} //(236,219,173)
`define CTLXBorder        { 5'd29, 6'd19, 5'd8} //(233,77,68)

module OLed_Volume_Display(
    input en,
    input CLK100MHZ,
    input [3:0] num,
    input border_on,       
    input volume_bar_on,   
    input [1:0] theme_sel,
    output reg [15:0] oled_data = 'd0,
    input [12:0] pixel_index,
    input freeze,
    input border_sel,
    input next
    );
    
    reg [15:0] color_volumebar_l;
    reg [15:0] color_volumebar_m;
    reg [15:0] color_volumebar_h;
    reg [15:0] color_bg;
    reg [15:0] color_bd;
    reg [15:0] oled_freeze [0:6143];
'''    

CODE2 = '''
    reg state = 0;
    
    always @ (posedge next)
        state <= 1;
    
    integer i;
    
    always @ (theme_sel, volume_bar_on, border_on) begin
        case ( theme_sel )
            'd0 : begin
                      color_volumebar_l <= volume_bar_on ? `CTDefaultVolumeBarL : `CTDefaultBackground;
                      color_volumebar_m <= volume_bar_on ? `CTDefaultVolumeBarM : `CTDefaultBackground;
                      color_volumebar_h <= volume_bar_on ? `CTDefaultVolumeBarH : `CTDefaultBackground;
                      color_bg          <= `CTDefaultBackground;
                      color_bd          <= border_on     ? `CTDefaultBorder : `CTDefaultBackground;
                  end
            'd1 : begin
                      color_volumebar_l <= volume_bar_on ? `CTLXVolumeBarL : `CTLXBackground;
                      color_volumebar_m <= volume_bar_on ? `CTLXVolumeBarM : `CTLXBackground;
                      color_volumebar_h <= volume_bar_on ? `CTLXVolumeBarH : `CTLXBackground;
                      color_bg          <= `CTLXBackground;
                      color_bd          <= border_on     ? `CTLXBorder : `CTLXBackground;
                  end
            'd2 : begin
                      color_volumebar_l <= volume_bar_on ? `CTLugeVolumeBarL : `CTLugeBackground;
                      color_volumebar_m <= volume_bar_on ? `CTLugeVolumeBarM : `CTLugeBackground;
                      color_volumebar_h <= volume_bar_on ? `CTLugeVolumeBarH : `CTLugeBackground;
                      color_bg          <=`CTLugeBackground;
                      color_bd          <= border_on ? `CTLugeBorder : `CTLugeBackground;
                  end
            'd3 : begin
                      color_volumebar_l <= volume_bar_on ? `CTRochorVolumeBarL : `CTRochorBackground;
                      color_volumebar_m <= volume_bar_on ? `CTRochorVolumeBarM : `CTRochorBackground;
                      color_volumebar_h <= volume_bar_on ? `CTRochorVolumeBarH : `CTRochorBackground;
                      color_bg          <=`CTRochorBackground;
                      color_bd          <= border_on ? `CTRochorBorder : `CTRochorBackground;
                  end
        endcase
    end
    
    always @ (pixel_index)
        oled_data <= oled_freeze[pixel_index];
    
    always @ (posedge CLK100MHZ) begin
        if (state == 1 && ! freeze) begin
            for (i=0; i<6144; i=i+1) begin
                oled_freeze[i] <= color_bg;
                if ((i % 96 < 30) || (65 < i % 96))
                    oled_freeze[i] <= color_bg;
                else if (i / 96 < 60 && i / 96 > 57)
                    oled_freeze[i] <= num >=  0 ? color_volumebar_l  : color_bg;
                else if (i / 96 < 57 && i / 96 > 54)
                    oled_freeze[i] <= num >=  1 ? color_volumebar_l  : color_bg;
                else if (i / 96 < 54 && i / 96 > 51)
                    oled_freeze[i] <= num >= 2  ? color_volumebar_l  : color_bg;
                else if (i / 96 < 51 && i / 96 > 48)
                    oled_freeze[i] <= num >= 3  ? color_volumebar_l  : color_bg;
                else if (i / 96 < 48 && i / 96 > 45)
                    oled_freeze[i] <= num >= 4  ? color_volumebar_l  : color_bg;
                else if (i / 96 < 45 && i / 96 > 42)
                    oled_freeze[i] <= num >= 5  ? color_volumebar_l  : color_bg;
                else if (i / 96 < 42 && i / 96 > 39)
                    oled_freeze[i] <= num >= 6  ? color_volumebar_m  : color_bg;
                else if (i / 96 < 39 && i / 96 > 36)
                    oled_freeze[i] <= num >= 7  ? color_volumebar_m  : color_bg;
                else if (i / 96 < 36 && i / 96 > 33)
                    oled_freeze[i] <= num >= 8  ? color_volumebar_m  : color_bg;
                else if (i / 96 < 33 && i / 96 > 30)
                    oled_freeze[i] <= num >= 9  ? color_volumebar_m  : color_bg;
                else if (i / 96 < 30 && i / 96 > 27)
                    oled_freeze[i] <= num >= 10 ? color_volumebar_m  : color_bg;
                else if (i / 96 < 27 && i / 96 > 24)
                    oled_freeze[i] <= num >= 11 ? color_volumebar_h  : color_bg;
                else if (i / 96 < 24 && i / 96 >  21)
                    oled_freeze[i] <= num >= 12 ? color_volumebar_h  : color_bg;
                else if (i / 96 <  21 && i / 96 >  18)
                    oled_freeze[i] <= num >= 13 ? color_volumebar_h  : color_bg;
                else if (i / 96 <  18 && i / 96 >  15)
                    oled_freeze[i] <= num >= 14 ? color_volumebar_h  : color_bg;
                else if (i / 96 <  15 && i / 96 >  12)
                    oled_freeze[i] <= num >= 15 ? color_volumebar_h  : color_bg;
                if (border_on) begin
                    if (border_sel) begin
                        if (i<'d96 || i>'d6046 || i%96 == 0 || i%96 == 95)
                            oled_freeze[i] <= color_bd;
                    end else begin
                        if (i<'d288 || i>'d5854 || i%96 < 3 || i%96 > 92)
                            oled_freeze[i] <= color_bd;
                    end
                end
            end
        end
    end
    
endmodule
'''

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
        sequence_of_pixels_16h.append(hex(int(rgb16b(fmt, i), 2))[2:])
    with open(sys.argv[-1], "w") as f:
        f.write(CODE1)
        f.write("    initial begin\n")
        tmp = 0
        for i in sequence_of_pixels_16h:
            f.write("        oled_freeze[%d] <= 'h" % (tmp,) + '0' * (4-len(i)) + i + ";\n")
            tmp += 1
        f.write("    end")
        f.write(CODE2)