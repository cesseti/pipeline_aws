def maiores_que_media(conteudo:dict)->list:
    media_valores = sum(conteudo.values()) / len(conteudo.values())

    lista_final= [(chave, valor) for chave, valor in conteudo.items() if valor > media_valores]
    
    lista_ordenada = sorted(lista_final, key=lambda item: item[1])

    return lista_ordenada

conteudo= {
    "arroz": 4.99,
    "feijão": 3.49,
    "macarrão": 2.99,
    "leite": 3.29,
    "pão": 1.99
}