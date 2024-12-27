from functools import reduce

def calcula_saldo(lancamentos):
    valores = map(lambda x: x[0] if x[1] == 'C' else -x[0], lancamentos)
    
    saldo_final = reduce(lambda acumulado, valor: acumulado + valor, valores)
    
    return saldo_final

lancamentos = [
    (200, 'D'),
    (300, 'C'),
    (100, 'C')
]