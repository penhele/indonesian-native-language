from lexer import tokenize
from parser import parse
from executor import evaluate

def main():
    while True:
        try:
            expr = input("Masukan ekspresi (or 'cabuttt' untuk keluar): ")
            if expr.lower() == 'cabuttt':
                break

            # Tokenize input
            tokens = list(tokenize(expr))

            # Parse tokens menjadi AST
            ast = parse(tokens)

            # Evaluasi AST
            result = evaluate(ast)

            print("Hasilnyo:", result)

        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()