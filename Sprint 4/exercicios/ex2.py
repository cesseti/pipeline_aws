def conta_vogais(texto:str)-> int:
    vogais = 'aeiouAEIOU'
    
    apenas_vogais = filter(lambda char: char in vogais, texto)
   
    return len(list(apenas_vogais))
   
conta_vogais('python')