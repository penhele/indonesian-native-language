from interpreter import Interpreter

def main():
    print("=== INTERPRETER BAHASA LO ===")
    interpreter = Interpreter()

    while True:
        try:
            line = input(">>> ")
            if line.strip().lower() == "keluar":
                break
            interpreter.execute(line)
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
