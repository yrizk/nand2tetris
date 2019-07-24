// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// we don't have chip for multiplication, but we can add 2 16bit buses. so lets
// loop and add r0 to itself r1 times. the result will be in r2. we'll jump when the count is right.

// initialization 
	@i // loaded into the A register
	M=0 // set i to 0 in memory
	@R2 // load into the A register
	M=0 // the value at R2 explicitly set to zero
(LOOP)
	@i // loaded into the M register
	D=M // D = i
	@R1 // loaded in the A register
	D=D-M // i=i-R1
	@END
	D;JGE // if i - R1 >= 0, terminate the loop
	@R0 // loaded into A register 
	D=M
	@R2 // loaded into M register
	M=D+M // R2 = R2 + R0
	@i // loads it into the M register
	M=M+1 // i++
	@LOOP
	0;JMP // GOTO LOOP
(END)
	@END
	0;JMP
