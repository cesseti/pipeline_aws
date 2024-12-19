# Etapa 1

    O primeiro passo dessa etapa foi a criação de uma imagem que executasse o arquivo abaixo: 
[carguru.py](carguru.py)

    Para isso utilizei o comando:
``` docker build -t <nome da imagem>``` 
    
    como pode ser visto na evidência abaixo: 
![criar-imagem-carguru](../evidencias/desafio/etapa-1/criar-imagem-carguru.png)

    e aqui pode-se ver que a imagem foi criada:
![imagem-criada-carguru](../evidencias/desafio/etapa-1/imagem-carguru-criada.png)

    Após isso foi necessária a criação e execução de um container a partir desta imagem: 
![criar-conteiner](../evidencias/desafio/etapa-1/criar-conteiner-etapa1.png)

    E aqui está ele criado:
![conteiner-criado](../evidencias/desafio/etapa-1/conteiner-etapa1-criado.png)

# Etapa 2

    Pergunta: É possível reutilizar um container ? 
    Resposta: Sim, e aqui está um container sendo reiniciado através do comando:
``` docker start -i <nome do conteiner>```

![reiniciando-um-conteiner](../evidencias/desafio/etapa-2/reiniciando-um-conteiner.png)


# Etapa 3

    O primeiro passo dessa etapa foi a criação de um arquivo python que aceitasse uma string, aplicasse o hash nela e a exibisse criptografada, tudo está feito nesse script:
[hash.py](./etapa-hash/hash.py)

    O segundo passo foi a criação de uma imagem para executar esse aquivo:
![mascarar-dados](../evidencias/desafio/etapa-hash/criar-imagem-mascarar-dados.png)

    e aqui pode-se ver que a imagem foi criada:
![imagem-criada-mascarar-dados](../evidencias/desafio/etapa-hash/imagem-mascarar-dados-criada.png)

    O terceiro e último passo foi a criação e execução do container através dessa imagem:
![criar-container](../evidencias/desafio/etapa-hash/criar-conteiner-etapa3-enviando-palavras.png)


