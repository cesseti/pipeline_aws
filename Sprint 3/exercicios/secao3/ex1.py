from datetime import datetime

nome = 'Carlos'

idade = 20

ano_atual = datetime.now().year

ano_nascimento = (ano_atual - idade)

cem_anos = (ano_nascimento + 100)

print(cem_anos)
