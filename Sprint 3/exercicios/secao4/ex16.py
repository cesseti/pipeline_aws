def soma_numeros(string_numeros):
    
    numeros = map(int, string_numeros.split(','))
    
    return sum(numeros)


string = "1,3,4,6,10,76"


resultado = soma_numeros(string)
print(resultado)
