from code import Code
from symbol_table import SymbolTable

class Parser:
    def __init__(self, filename):
        # Instance members
        self.filename = filename
        # coder object singleton
        self.c = Code()
        # symbol table to keep track of labels and variables
        self.tb = SymbolTable()
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
        
        # before main pass, parse all labels and make note of their addresses
        self.parse_labels()
        # after initializing, read file
        self.read_file()


    # loop through each line, and make note of each label and respective next line when encountered
    def parse_labels(self):
        with open(self.filename, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                t = self.command_type(line)
                if t != 'N':
                    if t == 'L':
                        # remove parenthesis from label command
                        label = line[1:-1]
                        if not self.tb.contains(label):
                            self.tb.add_entry(label, self.line_count)
                    else:
                        # labels aren't considered lines, so only increment line_count if t is an A or C instruction
                        self.line_count += 1


    def read_file(self):
        # open file from filename and automatically close after done
        with open(self.filename, 'r', encoding='utf-8') as file:
            # main line-searching loop
            for line in file:
                line = line.strip()
                if '//' in line:
                    line = line[:line.index('/')]
                # determine instruction type
                t = self.command_type(line)
                # ignore comments '//' and whitespace
                if t != 'N' and t != 'L':
                    # reset these each loop
                    self.wr = ""
                    self.op_code = ""
                    self.comp_code = ""
                    self.dest_code = ""
                    self.jump_code = ""

                    if t == 'C':
                        self.op_code = "111"
                        # Jump instruction (X;<JMP>)
                        if ';' in line:
                            self.configure_jump(line)
                        # Register manipulation instruction (dest=comp)
                        else:
                            self.configure_c_command(line)

                    # build final wr command from configured instance members
                    self.assemble_command(line)

                    # open filename.hack file and append final wr to file
                    with open(f"{self.filename[:-4]}.hack", "a") as file:
                        file.write(self.wr + '\n')

    # if ';' is in command, this function is invoked to configure instruction
    def configure_jump(self, line):
        # in any jump, dest_code is 000, comp_code could either be 000110 (D) or 101010 (0)
        self.dest_code = '000' 
        self.jump_code = self.c.jump(self.jump(line))
        self.comp_code = self.c.comp(self.dest(line))


    # if instruction is of the form (dest=comp), this function is invoked
    def configure_c_command(self, line):
        # Non jump C instructions have a 000 jump_code
        self.comp_code = self.c.comp(self.comp(line))
        self.dest_code = self.c.dest(self.dest(line))
        self.jump_code = "000"

    # Handles configuring wr with either variable/label resolution or @ literal
    def configure_a_command(self, line):
        # if t is A instruction, compose wr like this
        sym = self.symbol(line)
        if sym.isdigit():
            self.wr = self.c.dtob16(sym)
        else:
            if self.tb.contains(sym): 
                self.wr = self.c.dtob16(self.tb.get_addr(sym))
            else:
                self.wr = self.c.dtob16(self.tb.add_entry(sym)) 

    # Parent function calls C or A configuration baesd on op-code
    def assemble_command(self, line):
        if self.op_code == "111":
            # if t is C instruction, compose wr like this
            self.wr = self.op_code + self.comp_code + self.dest_code + self.jump_code
        else:
            self.configure_a_command(line)


    # A instruction base 10 int after the '@' symbol
    def symbol(self, line):
        return line[1:]

    # dest in C instruction (dest=comp)
    def dest(self, line):
        # technically, a jump is a C instruction, so handle these as edge case
        if ";" in line:
            return line[:line.index(";")]

        # otherwise, return the lhs in (dest=comp)
        return line[:line.index("=")]

    # comp (rhs) in C instruction (dest=comp)
    def comp(self, line):
        return line[line.index("=") + 1:]

    # jump mnemonic (ie. JMP, JGR) from C instruction
    def jump(self, line):
        return line[line.index(";") + 1:]

    # evaluates type of command and ignores comments and whitespace
    # If command is none of the below defined (including whitespace and
    # comments), it is ignored
    def command_type(self, line):
        if not line:
            return 'N'
        if line[0] == '@':
            return 'A'
        elif line[0] in "MDA0":
            return 'C'
        elif line[0] == '(':
            return 'L'
        else:
            return 'N'
