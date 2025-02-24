import csv

a_names = ['Leão', 'Tigre', 'Elefante', 'Girafa', 'Zebra', 'Macaco', 'Panda', 'Urso', 'Golfinho', 'Tubarão', 'Pinguim', 'Coruja', 'Cobra', 'Jacaré', 'Tartaruga', 'Borboleta', 'Abelha', 'Cavalo', 'Cachorro', 'Gato']

a_names.sort()

with open("animais.csv", mode="w", newline="", encoding="utf-8") as arquivo_csv:
    writer = csv.writer(arquivo_csv)
    
    for name in a_names :
        print(name),
        writer.writerow([name]) 