import re

TOKEN_SPECIFICATION = [
    ('ANGKA',    r'\d+'),            
    ('TAMBAH',   r'tambah'),         
    ('KURANG',   r'kurang'),         
    ('KALI',     r'kali'),           
    ('BAGI',     r'bagi'),           
    ('BUKA',     r'\('),             
    ('TUTUP',    r'\)'),             
    ('SKIP',     r'[ \t\n]+'),       
    ('ERROR',    r'.'),              
]

master_pattern = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in TOKEN_SPECIFICATION)

def tokenize(code):
    line_num = 1
    line_start = 0
    for mo in re.finditer(master_pattern, code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'SKIP':
            continue
        elif kind == 'ERROR':
            raise RuntimeError(f'{value!r} unexpected on line {line_num}')
        elif kind == 'ANGKA':
            value = int(value)
        yield kind, value
