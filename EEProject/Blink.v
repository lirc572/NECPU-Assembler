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
      0: inst = 32'd268468224;
      1: inst = 32'd201326592;
      2: inst = 32'd270532608;
      3: inst = 32'd203467434;
      4: inst = 32'd1277231104;
      5: inst = 32'd136314880;
      6: inst = 32'd272629888;
      7: inst = 32'd205520896;
      8: inst = 32'd809631745;
      9: inst = 32'd333447168;
      10: inst = 32'd266338312;
      11: inst = 32'd473956352;
      12: inst = 32'd1541406720;
      13: inst = 32'd333447168;
      14: inst = 32'd266338308;
      15: inst = 32'd1541406720;
    endcase
  end
endmodule
