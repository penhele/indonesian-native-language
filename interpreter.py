class Interpreter:
    def __init__(self):
        self.vars = {} 

    def evaluate_expression(self, expr):
    
        expr = expr.replace("tambah", "+")
        expr = expr.replace("kurang", "-")
        expr = expr.replace("kali", "*")
        expr = expr.replace("bagi", "/")

        
        for var in self.vars:
            expr = expr.replace(var, str(self.vars[var]))

        try:
            return eval(expr)
        except:
            print("❌ Ekspresi tidak valid:", expr)
            return None

    def execute(self, line):
        tokens = line.split()
        
        if len(tokens) >= 2:
            first_two = f"{tokens[0]} {tokens[1]}"
        else:
            first_two = tokens[0]

        if first_two == "gue punya":
            eq_index = tokens.index("=")
            var_name = tokens[2]
            value = " ".join(tokens[eq_index + 1:])
            result = self.evaluate_expression(value)
            self.vars[var_name] = result

        elif tokens[0] == "munculkan":
            value = " ".join(tokens[1:])
            result = self.evaluate_expression(value)
            print(result)
            
        else:
            print("❌ Perintah tidak dikenal:", line)
