from tokens import Token, TokenType


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
                if line[i] == '+':
                    token_type = TokenType.TAMBAH
                elif line[i] == '-':
                    token_type = TokenType.KURANG
                elif line[i] == '*':
                    token_type = TokenType.KALI
                elif line[i] == '/':
                    token_type = TokenType.BAGI
                elif line[i] == '=':
                    token_type = TokenType.SAMA
                self.tokens.append(Token(token_type, line[i], line_num))
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
