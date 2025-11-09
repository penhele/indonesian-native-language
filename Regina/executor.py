def evaluate(ast):
    if ast.type == 'ANGKA':
        return ast.value
    elif ast.type == 'TAMBAH':
        return evaluate(ast.left) + evaluate(ast.right)
    elif ast.type == 'KURANG':
        return evaluate(ast.left) - evaluate(ast.right)
    elif ast.type == 'KALI':
        return evaluate(ast.left) * evaluate(ast.right)
    elif ast.type == 'BAGI':
        return evaluate(ast.left) / evaluate(ast.right)