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

        if tokens[0] == "misal":
            var_name = tokens[1]
            value = " ".join(tokens[3:])
            result = self.evaluate_expression(value)
            self.vars[var_name] = result

        elif tokens[0] == "muncul":  # Print
            value = " ".join(tokens[1:])
            result = self.evaluate_expression(value)
            print(result)

        else:
            print("❌ Perintah tidak dikenal:", line)
