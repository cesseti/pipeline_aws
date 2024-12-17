import random

random_list = random.sample(range(500), 50)

n= len(random_list)

random_list.sort()

if n % 2 == 1:
    
    mediana = random_list[n // 2]
else:

    mediana = (random_list[n // 2 - 1] + random_list[n // 2]) /2

media = sum(random_list)/50
valor_minimo = min(random_list)
valor_maximo = max(random_list)

print(f"Media: {media:.2f}, Mediana: {mediana:.1f}, Mínimo: {valor_minimo}, Máximo: {valor_maximo}")