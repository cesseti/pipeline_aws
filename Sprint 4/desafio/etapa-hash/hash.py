import hashlib

# Input para receber string
string = input('Digite uma palavra para descobrir seu hash: ')

# Gera o hash SHA-1
hash_sha1 = hashlib.sha1(string.encode())

# Exibe o resultado
print(f"Esse é o hash da sua palavra: {hash_sha1.hexdigest()}")