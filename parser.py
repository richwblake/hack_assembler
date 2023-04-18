from code import Code

class Parser:
    def __init__(self, filename):
        # Instance members
        self.filename = filename
        # count of non-comment and non-whitespace lines
        self.line_count = 0
        # final binary self.writeout of each line
        self.wr = ""
        # operation code
        self.op_code = ""
        # comparison code in C instruction
        self.comp_code = ""
        # destination code in C instruction
        self.dest_code = ""
        # jump code in C instruction
        self.jump_code = ""

        # after initializing, read file
        self.read_file()


    def read_file(self):
        # create code object to transfer assembly mnemonic to respective binary
        c = Code()

        # open file from filename and automatically close after done
        with open(self.filename, 'r', encoding='utf-8') as file:
            # main line-searching loop
            for line in file:
                # determine instruction type
                t = self.command_type(line)
                # ignore comments '//' and whitespace
                if t != 'N':
                    # reset these each loop
                    self.wr = ""
                    self.op_code = ""
                    self.comp_code = ""
                    self.dest_code = ""
                    self.jump_code = ""
                    if t == 'A' or t == 'C':
                        self.line_count += 1
                    if t == 'A':
                        self.wr = c.dtob16(self.symbol(line))
                    if t == 'C':
                        self.wr = "111"
                        if ';' in line:
                            # handle dest jump here
                            self.dest_code = '000' 
                            self.jump_code = c.jump(self.jump(line))
                            self.comp_code = c.comp(self.dest(line))
                        else:
                            # handle dest and comp here
                            self.comp_code = c.comp(self.comp(line))
                            self.dest_code = c.dest(self.dest(line))
                            self.jump_code = "000"

                    self.wr = self.wr + self.op_code + self.comp_code + self.dest_code + self.jump_code

                    with open(f"{self.filename[:-4]}.hack", "a") as file:
                        if self.wr != "":
                            file.write(self.wr + '\n')


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


    # evaluates type of command and ignores comments and whitespace
    def command_type(self, line):
        if line[0] == '@':
            return 'A'
        elif line[0] in "MDA0":
            return 'C'
        elif line[0] == '(':
            return 'L'
        else:
            return 'N'
