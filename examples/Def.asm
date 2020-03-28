LLI $2, 1
LLI $1, 0
LUI $1, 32768
LLI $3, 1
LLI $4, 0
INV $4, $4
ADD $2, $2, $3
LLI $5, 4
BNE $4, 0
JMP $5
SW $2, $1, 0
