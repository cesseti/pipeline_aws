import json

with open('person.json', 'r') as arquivo:
    conteudo= json.load(arquivo)
    
print(conteudo)