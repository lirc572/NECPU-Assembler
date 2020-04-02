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
      0: inst = 32'h10005555;
      1: inst = 32'hc00aaaa;
      2: inst = 32'h10800000;
      3: inst = 32'hc800010;
      4: inst = 32'h10a08000;
      5: inst = 32'hca00000;
      6: inst = 32'h38202000;
      7: inst = 32'h8250000;
    endcase
  end
endmodule
