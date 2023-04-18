from code import Code

class Parser:
    def __init__(self, filename):
        self.file = open(filename, 'r', encoding='utf-8')
        self.filename = filename
        self.line_count = 0
        self.read_file()


    def read_file(self):
        c = Code()
        for line in self.file:
            t = self.command_type(line)
            if t != 'Comment' and t != 'Empty':
                wr = ""
                op_code = ""
                comp_code = ""
                dest_code = ""
                jump_code = ""
                if t != 'L':
                    self.line_count += 1
                if t == 'A':
                    wr = c.dtob16(self.symbol(line))
                if t == 'C':
                    wr = "111"
                    if ';' in line:
                        # handle dest jump here
                        dest_code = '000' 
                        jump_code = c.jump(self.jump(line))
                        comp_code = c.comp(self.dest(line))
                    else:
                        # handle dest and comp here
                        comp_code = c.comp(self.comp(line))
                        dest_code = c.dest(self.dest(line))
                        jump_code = "000"

                wr = wr + op_code + comp_code + dest_code + jump_code
                    
                with open(f"{self.filename[:-4]}.hack", "a") as file:
                    if wr != "":
                        file.write(wr + '\n')


    def symbol(self, line):
        return line[1:]

    def dest(self, line):
        if ";" in line:
            return line[:line.index(";")]

        return line[:line.index("=")]

    def comp(self, line):
        return line[line.index("=") + 1:]

    def jump(self, line):
        return line[line.index(";") + 1:]


    def command_type(self, line):
        if line[0] == '@':
            return 'A'
        elif line[0] == '(':
            return 'L'
        elif line[0] == '/' and line[1] == '/':
            return 'Comment'
        elif not line.strip():
            return 'Empty'
        else:
            return 'C'

