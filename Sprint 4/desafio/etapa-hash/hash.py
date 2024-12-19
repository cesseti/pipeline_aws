import hashlib

# Input para receber string
mensagem = input('Escreva uma mensagem: ')

# Gera o hash SHA-1
hash_sha1 = hashlib.sha1(mensagem.encode())

# Exibe o resultado
print(f"Esse é a sua mensagem: {mensagem}\nE esse é a sua mensagem em hash: {hash_sha1.hexdigest()}")