//For reference only, operators are directly translated from respective fields
//All fields of an instruction are showed
//This is not a valid source file!

 0 :  LUI  $10, $0 , 32768
 1 :  LLI  $10, $0 , 0
 2 :  LUI  $0 , $0 , 0
 3 :  LLI  $0 , $0 , 0
 4 :  LW   $1 , $0 , 0
 5 :  ADDI $0 , $0 , 1
 6 :  LW   $2 , $0 , 0
 7 :  SW   $1 , $10, 0
 8 :  LUI  $3 , $0 , 128
 9 :  LLI  $3 , $0 , 0
10 :  SUBI $3 , $3 , 1
11 :  LUI  $31, $0 , 0
12 :  LLI  $31, $0 , 10
13 :  BEQ  $3 , $0 , 0
14 :  JMP  $31, $0 , 0
15 :  SW   $2 , $10, 0
16 :  LUI  $3 , $0 , 256
17 :  LLI  $3 , $0 , 0
18 :  SUBI $3 , $3 , 1
19 :  LUI  $31, $0 , 0
20 :  LLI  $31, $0 , 18
21 :  BEQ  $3 , $0 , 0
22 :  JMP  $31, $0 , 0
23 :  LUI  $31, $0 , 0
24 :  LLI  $31, $0 , 7
25 :  JMP  $31, $0 , 0
