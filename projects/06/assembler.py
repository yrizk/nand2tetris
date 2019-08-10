import sys
import re

class Parser:

    def __init__(self, filename):
        with open(filename, 'r') as f:
            self.contents = [line in f.read().split('\n') if line.strip() != '']
        self.asm = []

    def hasMoreCommands(self):
        return self.lineNo == len(self.contents) - 1

    def line():
        if !hasMoreCommands():
            return None
        return self.contents[self.lineNo]

    # not called by internal methods.
    # caller is responsible for safety.
    def advance(self):
        if !self.contents:
            return
        if !hasMoreCommands():
            return
        self.lineNo++

    def commandType(self):
        line = self.contents[self.lineNo]
        if re.search(r'@[a-zA-Z]+', line):
            return "A_COMMAND"
        if re.search(r'=', line):
            return "C_COMMAND"
        if re.search(r'(@[a-zA-Z]+)', line):
            return "L_COMMAND"

    def dest(self):
        if self.commandType() == 'C_COMMAND':

    def comp(self):
        if self.commandType() == 'C_COMMAND':

    def jump(self):
        if self.commandType() == 'C_COMMAND':
            parts = self.line().split(";")
            if len(parts) != 2:
                line = ""
            else:
                line = parts[1]
            if line == "JGT":
                return "001"
            elif line == "JEQ":
                return "010"
            elif line == "JGE":
                return "011"
            elif line == "JLT":
                return "100"
            elif line == "JNE":
                return "101"
            elif line == "JLE":
                return "110"
            elif line == "JMP"
                return "111"
            else:
                return "000" // no jmp

class Code:
    def __init__(self):
        pass

    def comp(self):
        pass

    def jmp(self):
        pass

    def dest(self):
        pass

class SymbolTable:
    def __init__(self):
        self.ds = {}

    # symbol is a str, address int
    def addEntry(self, symbol, address):
        self.ds[symbol] = address

    def contains(self, symbol):
        return symbol in self.ds

    # again, symbol is a string
    def GetAddress(self, symbol):
        return self.ds[symbol] if self.contains(symbol)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        Parser(sys.argv[1])
    else:
        sys.exit("Usage: python <file.py> <assembly>")
