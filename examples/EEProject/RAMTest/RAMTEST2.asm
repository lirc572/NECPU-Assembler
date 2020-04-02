    LWI  $31, 0            //RAM  addr
    LWI  $30, 2147483648   //LED  addr
    LWI  $25, 2147500000   //OLED addr
    LWI  $28, 16           //Constant 16
HA:
    ADDi $31, $31, 1       //RAM addr  ++
    LW   $29, $31, 0       //Load pix
    SW   $29, $30, 0       //L -> LED
    SW   $29, $25, 0       //L -> OLED
    ADDi $25, $25, 1       //OLED addr ++

//    SRL  $29, $29, $28      //Load next pix
//    SW   $29, $30, 0        //U -> LED
//    SW   $29, $25, 0        //U -> OLED
//    ADDi $25, $25, 1        //OLED addr ++

    LWi  $20, 2083 //0.0005s
DEL1:
    SUBi $20, $20, 1
    BEQ  $20, 0
    JUMP DEL1

    JUMP HA