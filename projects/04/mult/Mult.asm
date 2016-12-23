// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.
// Program: Mult.asm
// Computes: R2=R0*R1
// Usage: Supply values in R0 and R1

        @R0
        D=M
        @multiplicand
        M=D                       // multiplicand = R0

        @R1
        D=M
        @multiplier
        M=D                       // multiplier = R1

        @R2
        M=0                       // R2 = 0
        @product
        M=0                       // variable product initialized to 0

(REPEATED_SUM_LOOP)
        @multiplier
        D=M
        @STOP
        D;JEQ                     // stop if multiplier has been decremented to 0
        @multiplier
        M=M-1                     // multiplier--

        @multiplicand
        D=M
        @product
        M=D+M                     // product = product + multiplicand

        @REPEATED_SUM_LOOP
        0;JMP                     // goto (REPEATED_SUM_LOOP)

(STOP)
        @product
        D=M
        @R2
        M=D                       // store to R2 the calculated product

(END)
        @END
        0;JMP                     // end program
