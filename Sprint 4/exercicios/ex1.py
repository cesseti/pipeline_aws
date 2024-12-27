with open('number.txt', 'r') as arquivo:
    numeros = arquivo.read().split()

numeros = list(map(int, numeros))

pares = list(filter(lambda x: x % 2 == 0, numeros))

pares_ordenados = sorted(pares, reverse= True)[:5]

soma = sum(pares_ordenados)

print(pares_ordenados)

print(soma)