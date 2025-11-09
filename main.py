from interpreter import Interpreter

def main():
    print("=== INDONESIAN NATURAL LANGUAGE ===")
    print("""
gue punya <variabel> = <nilai>
munculkan <variabel> / <nilai>
          """)
    print("="*35)
    
    interpreter = Interpreter()

    while True:
        try:
            line = input(">>> ")

            if not line:
                continue
            
            if line.strip().lower() == "keluar":
                break
            interpreter.execute(line)
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
