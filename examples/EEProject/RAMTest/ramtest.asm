        LWI $10, 2147483648 // $10 = addr of led
        LWI  $0, 0          // $0  = addr
        LW   $1, $0, 0      // $1  = MEM[addr]
        ADDi $0, $0, 1      // $0  = $0 + 1
        LW   $2, $0, 0      // $2  = MEM[addr]
LOOP:
        SW   $1, $10, 0     // Store to led regs


        LWI  $3, 0b100000000000000000000000 //25b
Delay:
        SUBi $3, $3, 1
        BEQ  $3, 0
        JUMP Delay

        SW   $2, $10, 0      // update led regs

        LWI  $3, 0b1000000000000000000000000  //26b
Delay2:
        SUBi $3, $3, 1
        BEQ  $3, 0
        JUMP Delay2

        JUMP LOOP