from lexers import Lexer
from tokens import Token, TokenType


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
        self.advance()  
        
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
        self.advance()  
        value = self.expression()
        print(value)
        self.skip_newlines()
    
    def if_statement(self):
        self.advance()  
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
            while self.current_token().type not in [TokenType.DEDENT, TokenType.KALO_KAGAK, TokenType.EOF]:
                self.advance()
        
        if self.current_token().type == TokenType.DEDENT:
            self.advance()
        
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
        self.advance() 
        condition_start = self.pos
        
        while True:
            self.pos = condition_start
            if not self.condition():
                while self.current_token().type not in [TokenType.DEDENT, TokenType.EOF]:
                    self.advance()
                if self.current_token().type == TokenType.DEDENT:
                    self.advance()
                break
            
            block_start = self.pos
            self.skip_newlines()
            
            if self.current_token().type == TokenType.INDENT:
                self.advance()
            
            while self.current_token().type not in [TokenType.DEDENT, TokenType.EOF]:
                self.skip_newlines()
                if self.current_token().type == TokenType.DEDENT:
                    break
                self.statement()
            
            if self.current_token().type == TokenType.DEDENT:
                self.advance()
    
    def for_statement(self):
        self.advance() 
        
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