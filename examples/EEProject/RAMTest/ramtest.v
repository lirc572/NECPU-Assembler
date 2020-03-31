`timescale 1ns / 1ps

//////////////////////////////////////////////////////////////////////////////////
// Company: lirc572
// Engineer: lirc572
// 
// Create Date: 
// Design Name: NECPU
// Module Name: InstMem
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
module instMem (
    input  [31:0]  address,
    output reg [31:0] inst
  );
  always @ (address) begin
    inst = 32'd0;
    case (address)
      0: inst = 32'd289439744;
      1: inst = 32'd222298112;
      2: inst = 32'd268435456;
      3: inst = 32'd201326592;
      4: inst = 32'd69206016;
      5: inst = 32'd671088641;
      6: inst = 32'd71303168;
      7: inst = 32'd136970240;
      8: inst = 32'd274727040;
      9: inst = 32'd207618048;
      10: inst = 32'd811794433;
      11: inst = 32'd333447168;
      12: inst = 32'd266338314;
      13: inst = 32'd476053504;
      14: inst = 32'd1541406720;
      15: inst = 32'd139067392;
      16: inst = 32'd274727168;
      17: inst = 32'd207618048;
      18: inst = 32'd811794433;
      19: inst = 32'd333447168;
      20: inst = 32'd266338322;
      21: inst = 32'd476053504;
      22: inst = 32'd1541406720;
      23: inst = 32'd333447168;
      24: inst = 32'd266338311;
      25: inst = 32'd1541406720;
    endcase
  end
endmodule
