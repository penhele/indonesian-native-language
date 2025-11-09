import enum

class TokenType(enum.Enum):
    TULIS = "tulis"   # print
    KALO = "kalo"     # if
    DARI = "dari"     # for
    SAMPE = "sampe"   # in range

def tokenize(kode: str):
    parts = kode.split()
    tokens = []

    for part in parts:
        found = None
        for token_type in TokenType:
            if part.lower() == token_type.value:
                found = token_type
                break
        
        if found:
            tokens.append(("KEYWORD", found))
        else:
            tokens.append(("IDENTIFIER", part))
    
    return tokens

def interpreter():
    print("Selamat datang")

    while True: 
        kode = input(">> ").strip()

        if kode.lower() == "exit":
            print("Keluar dari interpreter. Dadah~ 👋")
            break

        if not kode:
            continue
        
        tokens = tokenize(kode)

        if tokens and tokens[0][1] == TokenType.TULIS:
            isi = " ".join([t[1] if isinstance(t[1], str) else t[1].value for t in tokens[1:]])
            print(isi)

        else:
            print("⚠️ Perintah nggak dikenal, coba lagi!")

if __name__ == "__main__":
    interpreter()