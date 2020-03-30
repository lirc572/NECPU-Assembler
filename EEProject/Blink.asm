        LWI  $0, 2147483648         //addr of led (lower 16 bits)
        LWI  $1, 0b1010101010101010 //led output

LOOP:
        INV  $1, $1                 //invert led output
        SW   $1, $0, 0              //Store to actual led reg

        LWI  $2, 0b100000000000000000000000 //24bit... around 
Delay:
        SUBI $2, $2, 1
        BEQ  $2, 0
        JUMP Delay
        
        JUMP LOOP