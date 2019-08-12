import sys
import re

class Parser:

    def __init__(self, filename):
        with open(filename, 'r') as f:
            self.contents = [line in f.read().split('\n') if line.strip() != '']

    def hasMoreCommands(self):
        return self.lineNo == len(self.contents) - 1

    def line():
        if !hasMoreCommands():
            return None
        return self.contents[self.lineNo]

    def reset():
        self.lineNo = 0

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
            if self.line().find("=") == -1:
                return "000"
            line = self.line().split("=")[0] # not sure if this is required
            if line == "M":
                return "001"
            if line == "D":
                return "010"
            if line == "MD":
                return "011"
            if line == "A":
                return "100"
            if line == "AM":
                return "101"
            if line == "AD":
                return "110"
            if line == "AMD":
                return "111"

    def comp(self):
        if self.commandType() == 'C_COMMAND':
            parts = self.line().split("=")
            if len(parts) == 1:
                return "101010"
            line = parts[1].split(";")
            dest = parts[0]
            if len(line) == 2:
                line = line[0]
            if line == "0":
                return "0101010"
            if line == "1":
                return "0111111"
            if line == "-1":
                return "0111010"
            if line == "D":
                return "0001100"
            if line == "!D":
                return "0001111"
            if line == "-D":
                return "0001111"
            if line == "D+1":
                return "0011111"
            if line == "D-1":
                return "0001110"
            if dest == "D":
                if line == "M":
                    return "1110000"
                if line == "!M":
                    return "1110001"
                if line == "-M":
                    return "1110011"
                if line == "M+1":
                    return "1110111"
                if line == "M-1":
                    return "1110010"
                if line == "D+M":
                    return "1000010"
                if line == "D-M":
                    return "1010011"
                if line == "M-D":
                    return "1000111"
                if line == "D&M":
                    return "1000000"
                if line == "D|M":
                    return "1010101"
            else:
                if line == "A"
                    return "0110000"
                if line == "!A":
                    return "0110001"
                if line == "-A":
                    return "0110011"
                if line == "A+1":
                    return "0110111"
                if line == "A-1":
                    return "0110010"
                if line == "D+A":
                    return "0000010"
                if line == "D-A":
                    return "0010011"
                if line == "D-A":
                    return "0000111"
                if line == "D&A":
                    return "0000000"
                if line == "D|A":
                    return "0010101"

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
    def __init__(self, filename):
        self.parser = Parser(filename)

    def comp(self):
        return self.parser.comp()

    def jump(self):
        return self.parser.jump()

    def dest(self):
        return self.parser.dest()

class SymbolTable:

    def __init__(self):
        self.ds = {}
        self.addPredefinedSymbols()
        self.begAddress = 16

    def addPredefinedSymbols(self):
        for x in range(15):
            self.addEntry("R"+x, x)
        self.addEntry("SCREEN", 16384)
        self.addEntry("KBD", 24576)
        self.addEntry("SP", 0)
        self.addEntry("LCL", 1)
        self.addEntry("ARG", 2)
        self.addEntry("THIS", 3)
        self.addEntry("THAT", 4)

    # symbol is a str, address int
    def addEntry(self, symbol, address = -1):
        if address == -1:
            address = self.begAddress
            self.begAddress += 1
        self.ds[symbol] = address

    def contains(self, symbol):
        return symbol in self.ds

    # again, symbol is a string
    def getAddress(self, symbol):
        return self.ds[symbol] if self.contains(symbol)

def main():
    filename = sys.argv[1]
    code = Code(filename)
    parser = Parser(filename)
    st = SymbolTable()
    output = open(filename[:-4]+ '.hack', 'w+')
    while parser.hasMoreCommands():
        if parser.commandType() == 'L_COMMAND':
            st.addEntry(parser.line(), )
        line = parser.line()
        if parser.commandType() == 'A_COMMAND':



if __name__ == "__main__":
    if len(sys.argv) == 2:
        main()
    else:
        sys.exit("Usage: python <file.py> <assembly>")
