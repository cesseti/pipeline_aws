import random

num = [random.randint(1, 250) for _ in range(250)]

num.reverse()

print(num)