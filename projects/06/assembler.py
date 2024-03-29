import sys
import re

class Parser:

    def __init__(self, filename):
        self.contents = []
        self.lineMap = {}
        self.lineNo = 0
        line_no = 0
        self.L_COUNT = 0
        self.secondLineMap = {}
        with open(filename, 'r') as f:
            for line in f.read().split('\n'):
                if line.strip() != '' and not line.strip().startswith('//'):
                    mod_line = re.sub(r'//[-+*>()\[\]_</\s=a-zA-Z0-9]+', '', line).strip()
                    self.contents.append(mod_line)
                    if ')' in mod_line and '(' in mod_line:
                        self.secondLineMap[mod_line] = self.L_COUNT
                        self.L_COUNT += 1
                    self.lineMap[mod_line] = line_no
                    line_no += 1

    def hasMoreCommands(self):
        return self.lineNo < len(self.contents)

    def line(self):
        if not self.hasMoreCommands():
            return None
        return self.contents[self.lineNo]
    
    def lineNumber(self, line):
        return self.lineMap[line] - self.secondLineMap[line]

    def reset(self):
        self.lineNo = 0

    # not called by internal methods.
    # caller is responsible for safety.
    def advance(self):
        if not self.contents:
            return
        self.lineNo+=1

    def commandType(self):
        line = self.contents[self.lineNo]
        if re.search(r'@[a-zA-Z0-9]+', line):
            return "A_COMMAND"
        if re.search(r'=|;', line):
            return "C_COMMAND"
        if re.search(r'([a-zA-Z]+)', line):
            return "L_COMMAND"

    def isNumber(self):
        try:
            return int(re.sub(r'@R?', '', self.line()))
        except ValueError:
            return -1

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
            dest = ''
            line = ''
            jmp = ''
            if '=' in self.line() and ';' in self.line(): # full form
                tmp = self.line().split('=')
                dest = tmp[0]
                tmp2 = tmp[1].split(';')
                line = tmp[1]
                jmp = tmp[2]
            elif '=' in self.line():
                parts = self.line().split("=")
                dest = parts[0]
                line = parts[1]
            elif ';' in self.line():
                tmp = self.line().split(';')
                line = tmp[0]
                jmp = tmp[1]
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
            if line.find("M") > -1:
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
                if line == "A":
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
            elif line == "JMP":
                return "111"
            else:
                return "000"

class SymbolTable:
    def __init__(self):
        self.ds = {}
        self.addPredefinedSymbols()

    def addPredefinedSymbols(self):
        for x in range(15):
            self.addEntry("R"+str(x), x)
        self.addEntry("SCREEN", 16384)
        self.addEntry("KBD", 24576)
        self.addEntry("SP", 0)
        self.addEntry("LCL", 1)
        self.addEntry("ARG", 2)
        self.addEntry("THIS", 3)
        self.addEntry("THAT", 4)

    def dict(self):
        return self.ds

    # symbol is a str, address int
    def addEntry(self, symbol, address):
        self.ds[symbol] = address

    def contains(self, symbol):
        return symbol in self.ds

    # again, symbol is a string
    def getAddress(self, symbol):
        return self.ds[symbol] if self.contains(symbol) else None

# converts a decimal number (int) to a binary number (str)
def convert_to_binary(x):
    return "{0:016b}".format(x)

def main():
    filename = sys.argv[1]
    print("converting {} to hack".format(filename))
    parser = Parser(filename)
    st = SymbolTable()
    output = open(filename[:-4]+ '.hack', 'w+')
    # first pass, add the L_COMMANDS only.
    while parser.hasMoreCommands():
        line = parser.line()
        if parser.commandType() == 'L_COMMAND':
            st.addEntry(line[1:-1], parser.lineNumber(line))
        parser.advance()

    # 2nd pass: add A instructions and start writing to output
    parser.reset()
    address = 16
    while parser.hasMoreCommands():
        line = parser.line()
        if parser.commandType() == 'A_COMMAND':
            t = parser.isNumber()
            if t > -1:
                if not st.contains(line[1:]):
                    st.addEntry(line[1:], t)
            else:
                if not st.contains(line[1:]):
                    st.addEntry(line[1:], address)
                    address += 1
            output.write(convert_to_binary(st.getAddress(line[1:])))
            output.write("\n")
        if parser.commandType() == 'C_COMMAND':
            output.write("111" + parser.comp() + parser.dest() + parser.jump())
            output.write("\n")
        parser.advance()

if __name__ == "__main__":
    if len(sys.argv) == 2:
        main()
    else:
        sys.exit("Usage: python <file.py> <*.asm>")
