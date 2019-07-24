// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.
// Adds 1+...+100.
(INIT2)
@offset // a register
M=0
(KEYPRESSED)
	// check if we need to jump to the other section
	@KBD // D register
	D=M
	@KEYNOTPRESSED
	D;JEQ // jumps to the other section if D (which is M[KBD] = 0)
	// time to fill the screen
	@offset
	D=M
	@8192
	D=D-A  // offset - 8192
	@KEYNOTPRESSED
	D;JEQ
	@offset
	D=M
	@SCREEN // a register (overwriting @offset)
	A=D+A
	M=-1 // m[screen + offset] = 1
	@offset
	M=M+1 // increment offset.
	@KEYPRESSED
	0;JMP

(INIT)
	@offset // a register
	M=0
(KEYNOTPRESSED)
	// initialize state for clearing screen
	// checks if we should jump back to the other section
	@KBD
	D=M // sets D to M[KBD]
	@INIT2
	D;JGT // jumps to KEYPRESSED if D (which is M[KBD]) > 0
	// time to clear the screen
	@offset
	D=M
	@8192
	D=D-A  // offset - 8192
	@INIT
	D;JEQ
	@offset
	D=M
	@SCREEN // a register (overwriting @offset)
	A=D+A
	M=0 // m[screen + offset] = 0
	@offset
	M=M+1 // increment offset.
	@KEYNOTPRESSED
	0;JMP
