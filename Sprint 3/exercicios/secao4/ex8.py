l = ['maça', 'arara', 'audio', 'radio', 'radar', 'moto']

for palindromo in l:
    if palindromo == palindromo[::-1]:
        print(f'A palavra: {palindromo} é um palíndromo')
    else: 
        print(f'A palavra: {palindromo} não é um palíndromo')