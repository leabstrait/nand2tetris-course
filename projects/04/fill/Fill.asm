// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, the
// program clears the screen, i.e. writes "white" in every pixel.

// Put your code here.
// Program: Fill.asm
// Does: Fill screen black on any key press.
// Usage: Press any key, release.

(LOOP)
        @SCREEN
        D=A
        @current_pixel_block          // initialize current_pixel_block with base
        M=D                           // address of Screen Memory Map

        @8192                         // there are 16*32(=512) cols & 256 rows
        D=A                           // there are 32*256=8192 16bit blocks
        @no_of_blocks                 // initialize decrementor counter for no. of
        M=D                           // 16 bit blocks in SMM

        @KBD                          // set in data register the current value of
        D=M                           // Keyboard Memory Map

        @FILL_SCREEN_BLACK            // if KMM has non-zero content then
        D;JNE                         // goto FILL_SCREEN_BLACK

        @FILL_SCREEN_WHITE            // if KMM has non-zero content then
        D;JEQ                         // goto FILL_SCREEN_WHITE

(FILL_SCREEN_BLACK)
        @no_of_blocks
        D=M                           // if screen filled with black back to
        @LOOP                         // reading the key press
        D;JEQ

        @current_pixel_block          // set black to the content of currently
        A=M                           // selected pixel block
        M=-1
        @current_pixel_block          // increment pointer to SMM by 1
        M=M+1

        @no_of_blocks
        M=M-1

        @FILL_SCREEN_BLACK           // continue filling the screen until all
        0;JMP                        // all 16-bit blocks are done

(FILL_SCREEN_WHITE)
        @no_of_blocks
        D=M                           // if screen filled with WHITE back to
        @LOOP                         // reading the key press
        D;JEQ

        @current_pixel_block          // set WHITE to the content of currently
        A=M                           // selected pixel block
        M=0
        @current_pixel_block          // increment pointer to SMM by 1
        M=M+1

        @no_of_blocks
        M=M-1

        @FILL_SCREEN_WHITE           // continue filling the screen until all
        0;JMP                        // all 16-bit blocks are done
