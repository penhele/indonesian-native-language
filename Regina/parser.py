class ASTNode:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value
        self.left = None
        self.right = None

def parse(tokens):
    def parse_expression(tokens):
        node = parse_term(tokens)
        while tokens and tokens[0][0] in ('TAMBAH', 'KURANG'):
            op = tokens.pop(0)
            right = parse_term(tokens)
            new_node = ASTNode(op[0], op[1])
            new_node.left = node
            new_node.right = right
            node = new_node
        return node

    def parse_term(tokens):
        node = parse_factor(tokens)
        while tokens and tokens[0][0] in ('KALI', 'BAGI'):
            op = tokens.pop(0)
            right = parse_factor(tokens)
            new_node = ASTNode(op[0], op[1]) 
            new_node.left = node
            new_node.right = right
            node = new_node
        return node

    def parse_factor(tokens):
        token = tokens.pop(0)
        if token[0] == 'ANGKA':
            return ASTNode('ANGKA', token[1])
        elif token[0] == 'BUKA':
            node = parse_expression(tokens)
            if tokens.pop(0)[0] != 'TUTUP':
                raise RuntimeError('Harus ada tutup kurung setelah ekspresi')
            return node
        else:
            raise RuntimeError(f'Unexpected token: {token}')

    return parse_expression(tokens)