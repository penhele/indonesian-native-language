from interpreter import Interpreter


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
            code = '\n'.join(code_buffer)
            print("\n--- HASIL EKSEKUSI ---")
            interpreter = Interpreter()
            interpreter.execute(code)
            code_buffer = []

if __name__ == "__main__":
    main()