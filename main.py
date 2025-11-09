import re
from enum import Enum

class TokenType(Enum):
    # Kata kunci
    GUE_PUNYA = "gue_punya"  # deklarasi variabel
    KALO = "kalo"  # if
    KALO_KAGAK = "kalo_kagak"  # else
    SELAMA = "selama"  # while
    DARI = "dari"  # for in range
    SAMPE = "sampe"  # to
    TULIS = "tulis"  # print
    BACA = "baca"  # input
    
    # Tipe data
    ANGKA = "angka"
    TEKS = "teks"
    BENER_SALAH = "bener_salah"
    
    # Operator
    TAMBAH = "+"
    KURANG = "-"
    KALI = "*"
    BAGI = "/"
    
    # Perbandingan
    SAMA_DENGAN = "sama dengan"
    KAGAK_SAMA = "kagak sama"
    LEBIH_GEDE = "lebih gede dari"
    LEBIH_KECIL = "lebih kecil dari"
    GEDE_SAMA = "gede sama dengan"
    KECIL_SAMA = "kecil sama dengan"
    
    # Lainnya
    IDENTIFIER = "identifier"
    NUMBER = "number"
    STRING = "string"
    TRUE = "bener"
    FALSE = "salah"
    NEWLINE = "newline"
    INDENT = "indent"
    DEDENT = "dedent"
    EOF = "eof"

class Token:
    def __init__(self, type, value, line=0):
        self.type = type
        self.value = value
        self.line = line
    
    def __repr__(self):
        return f"Token({self.type}, {self.value})"

class Lexer:
    def __init__(self, code):
        self.code = code
        self.pos = 0
        self.line = 1
        self.tokens = []
        self.indent_stack = [0]
    
    def tokenize(self):
        lines = self.code.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            if not line.strip():
                continue
            
            # Hitung indentasi
            indent = len(line) - len(line.lstrip())
            
            # Proses indent/dedent
            if indent > self.indent_stack[-1]:
                self.indent_stack.append(indent)
                self.tokens.append(Token(TokenType.INDENT, indent, line_num))
            elif indent < self.indent_stack[-1]:
                while self.indent_stack[-1] > indent:
                    self.indent_stack.pop()
                    self.tokens.append(Token(TokenType.DEDENT, indent, line_num))
            
            # Tokenize line
            self.tokenize_line(line.strip(), line_num)
            self.tokens.append(Token(TokenType.NEWLINE, '\n', line_num))
        
        # Cleanup dedents
        while len(self.indent_stack) > 1:
            self.indent_stack.pop()
            self.tokens.append(Token(TokenType.DEDENT, 0, line_num))
        
        self.tokens.append(Token(TokenType.EOF, None, line_num))
        return self.tokens
    
    def tokenize_line(self, line, line_num):
        i = 0
        while i < len(line):
            # Skip whitespace
            if line[i].isspace():
                i += 1
                continue
            
            # String
            if line[i] in '"\'':
                quote = line[i]
                i += 1
                start = i
                while i < len(line) and line[i] != quote:
                    i += 1
                self.tokens.append(Token(TokenType.STRING, line[start:i], line_num))
                i += 1
                continue
            
            # Numbers
            if line[i].isdigit():
                start = i
                while i < len(line) and (line[i].isdigit() or line[i] == '.'):
                    i += 1
                num_str = line[start:i]
                value = float(num_str) if '.' in num_str else int(num_str)
                self.tokens.append(Token(TokenType.NUMBER, value, line_num))
                continue
            
            # Operators
            if line[i] in '+-*/=':
                self.tokens.append(Token(TokenType(line[i]), line[i], line_num))
                i += 1
                continue
            
            # Keywords dan identifiers
            start = i
            while i < len(line) and (line[i].isalnum() or line[i] == '_'):
                i += 1
            
            word = line[start:i]
            
            # Cek multi-word keywords
            remaining = line[i:].lstrip()
            
            if word == "gue" and remaining.startswith("punya"):
                self.tokens.append(Token(TokenType.GUE_PUNYA, "gue punya", line_num))
                i += len("punya") + (len(line[i:]) - len(remaining))
            elif word == "kalo" and remaining.startswith("kagak"):
                self.tokens.append(Token(TokenType.KALO_KAGAK, "kalo kagak", line_num))
                i += len("kagak") + (len(line[i:]) - len(remaining))
            elif word == "sama" and remaining.startswith("dengan"):
                self.tokens.append(Token(TokenType.SAMA_DENGAN, "sama dengan", line_num))
                i += len("dengan") + (len(line[i:]) - len(remaining))
            elif word == "kagak" and remaining.startswith("sama"):
                self.tokens.append(Token(TokenType.KAGAK_SAMA, "kagak sama", line_num))
                i += len("sama") + (len(line[i:]) - len(remaining))
            elif word == "lebih" and remaining.startswith("gede dari"):
                self.tokens.append(Token(TokenType.LEBIH_GEDE, "lebih gede dari", line_num))
                i += len("gede dari") + (len(line[i:]) - len(remaining))
            elif word == "lebih" and remaining.startswith("kecil dari"):
                self.tokens.append(Token(TokenType.LEBIH_KECIL, "lebih kecil dari", line_num))
                i += len("kecil dari") + (len(line[i:]) - len(remaining))
            elif word == "gede" and remaining.startswith("sama dengan"):
                self.tokens.append(Token(TokenType.GEDE_SAMA, "gede sama dengan", line_num))
                i += len("sama dengan") + (len(line[i:]) - len(remaining))
            elif word == "kecil" and remaining.startswith("sama dengan"):
                self.tokens.append(Token(TokenType.KECIL_SAMA, "kecil sama dengan", line_num))
                i += len("sama dengan") + (len(line[i:]) - len(remaining))
            elif word == "kalo":
                self.tokens.append(Token(TokenType.KALO, word, line_num))
            elif word == "selama":
                self.tokens.append(Token(TokenType.SELAMA, word, line_num))
            elif word == "dari":
                self.tokens.append(Token(TokenType.DARI, word, line_num))
            elif word == "sampe":
                self.tokens.append(Token(TokenType.SAMPE, word, line_num))
            elif word == "tulis":
                self.tokens.append(Token(TokenType.TULIS, word, line_num))
            elif word == "baca":
                self.tokens.append(Token(TokenType.BACA, word, line_num))
            elif word == "bener":
                self.tokens.append(Token(TokenType.TRUE, True, line_num))
            elif word == "salah":
                self.tokens.append(Token(TokenType.FALSE, False, line_num))
            else:
                self.tokens.append(Token(TokenType.IDENTIFIER, word, line_num))

class Interpreter:
    def __init__(self):
        self.variables = {}
        self.tokens = []
        self.pos = 0
    
    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return Token(TokenType.EOF, None)
    
    def advance(self):
        self.pos += 1
    
    def skip_newlines(self):
        while self.current_token().type == TokenType.NEWLINE:
            self.advance()
    
    def execute(self, code):
        lexer = Lexer(code)
        self.tokens = lexer.tokenize()
        self.pos = 0
        
        try:
            while self.current_token().type != TokenType.EOF:
                self.skip_newlines()
                if self.current_token().type == TokenType.EOF:
                    break
                self.statement()
        except Exception as e:
            print(f"Error: {e}")
    
    def statement(self):
        token = self.current_token()
        
        if token.type == TokenType.GUE_PUNYA:
            self.declaration()
        elif token.type == TokenType.TULIS:
            self.print_statement()
        elif token.type == TokenType.KALO:
            self.if_statement()
        elif token.type == TokenType.SELAMA:
            self.while_statement()
        elif token.type == TokenType.DARI:
            self.for_statement()
        elif token.type == TokenType.IDENTIFIER:
            self.assignment()
        else:
            self.advance()
    
    def declaration(self):
        self.advance()  # skip 'gue punya'
        
        if self.current_token().type == TokenType.IDENTIFIER:
            var_name = self.current_token().value
            self.advance()
            
            if self.current_token().value == '=':
                self.advance()
                value = self.expression()
                self.variables[var_name] = value
            
            self.skip_newlines()
    
    def assignment(self):
        var_name = self.current_token().value
        self.advance()
        
        if self.current_token().value == '=':
            self.advance()
            value = self.expression()
            self.variables[var_name] = value
        
        self.skip_newlines()
    
    def print_statement(self):
        self.advance()  # skip 'tulis'
        value = self.expression()
        print(value)
        self.skip_newlines()
    
    def if_statement(self):
        self.advance()  # skip 'kalo'
        condition = self.condition()
        
        self.skip_newlines()
        
        if self.current_token().type == TokenType.INDENT:
            self.advance()
        
        if condition:
            while self.current_token().type not in [TokenType.DEDENT, TokenType.KALO_KAGAK, TokenType.EOF]:
                self.skip_newlines()
                if self.current_token().type in [TokenType.DEDENT, TokenType.KALO_KAGAK]:
                    break
                self.statement()
        else:
            # Skip if block
            while self.current_token().type not in [TokenType.DEDENT, TokenType.KALO_KAGAK, TokenType.EOF]:
                self.advance()
        
        if self.current_token().type == TokenType.DEDENT:
            self.advance()
        
        # Handle else
        if self.current_token().type == TokenType.KALO_KAGAK:
            self.advance()
            self.skip_newlines()
            
            if self.current_token().type == TokenType.INDENT:
                self.advance()
            
            if not condition:
                while self.current_token().type not in [TokenType.DEDENT, TokenType.EOF]:
                    self.skip_newlines()
                    if self.current_token().type == TokenType.DEDENT:
                        break
                    self.statement()
            else:
                while self.current_token().type not in [TokenType.DEDENT, TokenType.EOF]:
                    self.advance()
            
            if self.current_token().type == TokenType.DEDENT:
                self.advance()
    
    def while_statement(self):
        self.advance()  # skip 'selama'
        condition_start = self.pos
        
        while True:
            self.pos = condition_start
            if not self.condition():
                # Skip while block
                while self.current_token().type not in [TokenType.DEDENT, TokenType.EOF]:
                    self.advance()
                if self.current_token().type == TokenType.DEDENT:
                    self.advance()
                break
            
            block_start = self.pos
            self.skip_newlines()
            
            if self.current_token().type == TokenType.INDENT:
                self.advance()
            
            # Execute block
            while self.current_token().type not in [TokenType.DEDENT, TokenType.EOF]:
                self.skip_newlines()
                if self.current_token().type == TokenType.DEDENT:
                    break
                self.statement()
            
            if self.current_token().type == TokenType.DEDENT:
                self.advance()
    
    def for_statement(self):
        self.advance()  # skip 'dari'
        
        if self.current_token().type != TokenType.IDENTIFIER:
            raise Exception("Expected variable name")
        
        var_name = self.current_token().value
        self.advance()
        
        if self.current_token().value != '=':
            raise Exception("Expected =")
        self.advance()
        
        start = self.expression()
        
        if self.current_token().type != TokenType.SAMPE:
            raise Exception("Expected 'sampe'")
        self.advance()
        
        end = self.expression()
        
        block_start = self.pos
        self.skip_newlines()
        
        if self.current_token().type == TokenType.INDENT:
            indent_pos = self.pos
            self.advance()
        
        for i in range(int(start), int(end) + 1):
            self.variables[var_name] = i
            self.pos = block_start
            self.skip_newlines()
            
            if self.current_token().type == TokenType.INDENT:
                self.advance()
            
            while self.current_token().type not in [TokenType.DEDENT, TokenType.EOF]:
                self.skip_newlines()
                if self.current_token().type == TokenType.DEDENT:
                    break
                self.statement()
        
        # Skip to end of block
        while self.current_token().type not in [TokenType.DEDENT, TokenType.EOF]:
            self.advance()
        
        if self.current_token().type == TokenType.DEDENT:
            self.advance()
    
    def condition(self):
        left = self.expression()
        
        op = self.current_token()
        
        if op.type == TokenType.SAMA_DENGAN:
            self.advance()
            right = self.expression()
            return left == right
        elif op.type == TokenType.KAGAK_SAMA:
            self.advance()
            right = self.expression()
            return left != right
        elif op.type == TokenType.LEBIH_GEDE:
            self.advance()
            right = self.expression()
            return left > right
        elif op.type == TokenType.LEBIH_KECIL:
            self.advance()
            right = self.expression()
            return left < right
        elif op.type == TokenType.GEDE_SAMA:
            self.advance()
            right = self.expression()
            return left >= right
        elif op.type == TokenType.KECIL_SAMA:
            self.advance()
            right = self.expression()
            return left <= right
        
        return bool(left)
    
    def expression(self):
        result = self.term()
        
        while self.current_token().value in ['+', '-']:
            op = self.current_token().value
            self.advance()
            if op == '+':
                result += self.term()
            else:
                result -= self.term()
        
        return result
    
    def term(self):
        result = self.factor()
        
        while self.current_token().value in ['*', '/']:
            op = self.current_token().value
            self.advance()
            if op == '*':
                result *= self.factor()
            else:
                result /= self.factor()
        
        return result
    
    def factor(self):
        token = self.current_token()
        
        if token.type == TokenType.NUMBER:
            self.advance()
            return token.value
        elif token.type == TokenType.STRING:
            self.advance()
            return token.value
        elif token.type == TokenType.TRUE:
            self.advance()
            return True
        elif token.type == TokenType.FALSE:
            self.advance()
            return False
        elif token.type == TokenType.IDENTIFIER:
            self.advance()
            if token.value in self.variables:
                return self.variables[token.value]
            raise Exception(f"Variable '{token.value}' not defined")
        elif token.type == TokenType.BACA:
            self.advance()
            return input()
        
        raise Exception(f"Unexpected token: {token}")

def main():
    print("=" * 60)
    print("INTERPRETER BAHASA PEMROGRAMAN BETAWI")
    print("=" * 60)
    print("\nContoh syntax:")
    print("  gue punya angka = 10")
    print("  tulis angka")
    print("  kalo angka lebih gede dari 5")
    print("      tulis \"angka gede banget!\"")
    print("\nKetik 'contoh' untuk melihat program contoh")
    print("Ketik 'keluar' untuk exit")
    print("Ketik 'jalanin' setelah menulis kode untuk execute")
    print("=" * 60)
    
    code_buffer = []
    
    while True:
        if not code_buffer:
            line = input("\n>>> ").strip()
        else:
            line = input("... ").strip()
        
        if line.lower() == 'keluar':
            print("Dadah!")
            break
        
        if line.lower() == 'contoh':
            contoh = """gue punya nama = "Budi"
tulis "Halo"
tulis nama

gue punya angka = 10
kalo angka lebih gede dari 5
    tulis "Angka gede banget!"
kalo kagak
    tulis "Angka kecil"

dari i = 1 sampe 5
    tulis i

gue punya x = 0
selama x lebih kecil dari 3
    tulis x
    x = x + 1"""
            
            print("\n--- CONTOH PROGRAM ---")
            print(contoh)
            print("--- HASIL EKSEKUSI ---")
            interpreter = Interpreter()
            interpreter.execute(contoh)
            continue
        
        if line.lower() == 'jalanin':
            if code_buffer:
                code = '\n'.join(code_buffer)
                print("\n--- HASIL EKSEKUSI ---")
                interpreter = Interpreter()
                interpreter.execute(code)
                code_buffer = []
            else:
                print("Gak ada kode yang mau dijalanin!")
            continue
        
        if line:
            code_buffer.append(line)
        elif code_buffer:
            # Empty line with code buffer means execute
            code = '\n'.join(code_buffer)
            print("\n--- HASIL EKSEKUSI ---")
            interpreter = Interpreter()
            interpreter.execute(code)
            code_buffer = []

if __name__ == "__main__":
    main()