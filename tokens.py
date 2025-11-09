from enum import Enum

class TokenType(Enum):
    # Kata kunci
    GUE_PUNYA = "gue_punya"
    KALO = "kalo"
    KALO_KAGAK = "kalo_kagak"
    SELAMA = "selama"
    DARI = "dari"
    SAMPE = "sampe"
    TULIS = "tulis"
    BACA = "baca"
    
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
