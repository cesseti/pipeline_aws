def calcular_valor_maximo(operadores,operandos) -> float:
    
    def aplicar_operador(par):
        a, b = par[1]
        operador = par[0]
        if operador == '+':
            return a + b
        elif operador == '-':
            return a - b
        elif operador == '*':
            return a * b
        elif operador == '/':
            return a / b
        elif operador == '%':
            return a % b
   
    pares = zip(operadores,operandos)

    resultado = list(map(aplicar_operador, pares))

    return max(resultado)