def dividir_lista(lista):

    tamanho = len(lista)
    parte = tamanho // 3 
    resto = tamanho % 3   


    primeira_parte = lista[:parte + (1 if resto > 0 else 0)]
    segunda_parte = lista[parte + (1 if resto > 0 else 0):2 * parte + (1 if resto > 1 else 0)]
    terceira_parte = lista[2 * parte + (1 if resto > 1 else 0):]

    return primeira_parte, segunda_parte, terceira_parte


lista = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
p1, p2, p3 = dividir_lista(lista)
print(f"{p1} {p2} {p3}")
