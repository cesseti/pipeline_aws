import csv

with open('estudantes.csv', 'r') as arquivo:
    leitor = csv.reader(arquivo)
    
    estudantes = []
    
    for linha in leitor:
        nome = linha[0]
        
        notas = list(map(int, linha[1:]))
        
        maiores_notas = sorted(notas, reverse=True)[:3]
        
        media = round(sum(maiores_notas) / 3, 2)
        
        estudantes.append((nome, maiores_notas, media))
    
    estudantes = sorted(estudantes, key=lambda x: x[0])


for nome, notas, media in estudantes:
    print(f"Nome: {nome} Notas: {notas} Média: {media}")
