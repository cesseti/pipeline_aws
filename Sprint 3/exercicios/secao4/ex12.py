def potencia(num):
    return num **2

def my_map(numeros, potencia):
    return[potencia(numero) for numero in numeros]

numeros= [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

resultado = my_map(numeros, potencia)

print(resultado)