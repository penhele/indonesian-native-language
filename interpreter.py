from tokens import TokenType, Token
from lexer import Lexer

class Interpreter:
    def __init__(self):
        self.variables = {}
        self.tokens = []
        self.pos = 0
