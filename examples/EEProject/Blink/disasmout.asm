//For reference only, operators are directly translated from respective fields
//All fields of an instruction are showed
//This is not a valid source file!

 0 :  LUI  $0 , $0 , 32768
 1 :  LLI  $0 , $0 , 0
 2 :  LUI  $1 , $0 , 0
 3 :  LLI  $1 , $0 , 43690
 4 :  INV  $1 , $1 , $0  0
 5 :  SW   $1 , $0 , 0
 6 :  LUI  $2 , $0 , 128
 7 :  LLI  $2 , $0 , 0
 8 :  SUBI $2 , $2 , 1
 9 :  LUI  $31, $0 , 0
10 :  LLI  $31, $0 , 8
11 :  BEQ  $2 , $0 , 0
12 :  JMP  $31, $0 , 0
13 :  LUI  $31, $0 , 0
14 :  LLI  $31, $0 , 4
15 :  JMP  $31, $0 , 0
