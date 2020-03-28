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
`define InstBusWidth  32
`define InstAddrBus   32
module instMem (
    input  [`InstAddrBus-1:0]  address,
    output reg [`InstBusWidth-1:0] inst
  );
  always @ (address) begin
    inst = 32'd0;
    case (address)
      0: inst = 32'd205520897;
      1: inst = 32'd203423744;
      2: inst = 32'd270565376;
      3: inst = 32'd207618049;
      4: inst = 32'd209715200;
      5: inst = 32'd1283719168;
      6: inst = 32'd608311296;
      7: inst = 32'd211812356;
      8: inst = 32'd545259520;
      9: inst = 32'd1486880768;
      10: inst = 32'd138477568;
    endcase
  end
endmodule
