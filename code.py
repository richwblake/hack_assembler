import re

class Code:
    # initialize tables that map each (dest=comp;jump) to their contracted binary representation
    def __init__(self):
        self.comp_table = {
                "0": "101010",
                "1": "111111",
                "-1": "111010",
                "D": "001100",
                "S": "110000",
                "!D": "001101",
                "!S": "110001",
                "-D": "001111",
                "-S": "110011",
                "D+1": "011111",
                "S+1": "110111",
                "D-1": "001110",
                "S-1": "110010",
                "D+S": "000010",
                "D-S": "010011",
                "S-D": "000111",
                "D&S": "000000",
                "D|S": "010101",
                }

        self.dest_table = {
                "null": "000",
                "M": "001",
                "D": "010",
                "DM": "011",
                "MD": "011",
                "A": "100",
                "AM": "101",
                "AD": "110",
                "ADM": "111",
                "AMD": "111",
                }

        self.jump_table = {
                "null": "000",
                "JGT": "001",
                "JEQ": "010",
                "JGE": "011",
                "JLT": "100",
                "JNE": "101",
                "JLE": "110",
                "JMP": "111",
                }


    # determines d bits in instruction given an expression
    # oooacccccc'ddd'jjj
    def dest(self, expr):
        return self.dest_table.get(expr.strip())

    # determines c bits in instruction given an expression
    # oooa'cccccc'dddjjj
    def comp(self, expr):
        # subs both A and M for placeholder S to decrease size of comp_table
        gen_str = re.sub("[AM]", "S", expr.strip())
        c = self.comp_table.get(gen_str)

        return self.aBit(expr) + c

    # determines value of a-bit in instruction given an expression
    # ooo'a'ccccccdddjjj
    def aBit(self, expr):
        return "1" if "M" in expr else "0"
    
    # determines value of jump bits in instruction given an expression
    # oooaccccccddd'jjj'
    def jump(self, expr):
        return self.jump_table.get(expr.strip())

    # converts base 10 int d to 16 bit binary int of type str
    def dtob16(self, d):
        b = format(int(d), 'b')
        for i in range(0, 16 - len(b)):
            b = '0' + b

        return b
