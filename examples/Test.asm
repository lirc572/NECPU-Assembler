        LLI  $2, 1
        LLI  $1, 0
        LLI  $1, 32768
        LLI  $3, 1
        LLI  $4, 0
LOOP:   INV  $4, $4
        ADD  $2, $2, $3
        BNE  $4, 0
        JUMP LOOP
        SW   $2, $1, 0
