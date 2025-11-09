from interpreter import Interpreter

def main():
    print("=" * 60)
    print("INTERPRETER BAHASA PEMROGRAMAN BETAWI")
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
        
        if line.lower() == 'jalanin':
            code = '\n'.join(code_buffer)
            interpreter = Interpreter()
            interpreter.execute(code)
            code_buffer = []
            continue
        
        if line:
            code_buffer.append(line)

if __name__ == "__main__":
    main()
