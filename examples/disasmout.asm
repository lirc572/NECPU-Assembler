//For reference only, operators are directly translated from respective fields
//All fields of an instruction are showed
//This is not a valid source file!

 0 :  LLI  $2 , $0 , 1
 1 :  LLI  $1 , $0 , 0
 2 :  LLI  $1 , $0 , 32768
 3 :  LLI  $3 , $0 , 1
 4 :  LLI  $4 , $0 , 0
 5 :  INV  $4 , $4 , $0  0
 6 :  ADD  $2 , $2 , $3  0
 7 :  BNE  $4 , $0 , 0
 8 :  LUI  $31, $0 , 0
 9 :  LLI  $31, $0 , 5
10 :  JMP  $31, $0 , 0
11 :  SW   $2 , $1 , 0
