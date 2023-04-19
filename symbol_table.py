from pprint import pprint

class SymbolTable:
    def __init__(self):
        # first 15 indices of ROM reserved, start at index 16 to allocate space for new variables
        self.current_rom_addr = 16
        
        # table holds all predefined and user-defined variables
        self.table = {
                "R0": "0",
                "R1": "1",
                "R2": "2",
                "R3": "3",
                "R4": "4",
                "R5": "5",
                "R6": "6",
                "R7": "7",
                "R8": "8",
                "R9": "9",
                "R10": "10",
                "R11": "11",
                "R12": "12",
                "R13": "13",
                "R14": "14",
                "R15": "15",
                "SCREEN": "16384",
                "KBD": "24576",
                "SP": "0",
                "LCL": "1",
                "ARG": "2",
                "THIS": "3",
                "THAT": "4"
                }


    def add_entry(self, symbol, addr=-1):
        if symbol not in self.table:
            if addr == -1:
                self.table[symbol] = self.current_rom_addr
                self.current_rom_addr += 1
            else:
                self.table[symbol] = addr

        return addr if addr != -1 else self.current_rom_addr - 1

    def contains(self, symbol):
        return symbol in self.table

    def get_addr(self, symbol):
        if symbol in self.table:
            return self.table.get(symbol)
