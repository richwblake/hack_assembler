import re

class Code:
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


    def dest(self, expr):
        return self.dest_table.get(expr.strip())

    def comp(self, expr):
        gen_str = re.sub("[AM]", "S", expr.strip())
        c = self.comp_table.get(gen_str)

        if "M" in expr:
            c = "1" + c
        else:
            c = "0" + c

        return c
    
    def jump(self, expr):
        return self.jump_table.get(expr.strip())

    def dtob16(self, d):
        b = format(int(d), 'b')
        for i in range(0, 16 - len(b)):
            b = '0' + b

        return b


