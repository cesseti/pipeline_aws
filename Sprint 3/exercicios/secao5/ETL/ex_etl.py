import re

def etapa1():
    with open("actors.csv", 'r', encoding='utf-8') as arquivo:
        linhas = arquivo.readlines()

    cabecalho = linhas[0]
    dados = linhas[1:]

    ator_mais_filmes = ""
    max_num_filmes = 0

    for linha in dados:
        # Corrigir vírgulas dentro de aspas
        linha_corrigida = re.sub(r'\"(.*?)\"', lambda x: x.group(0).replace(",", ""), linha.strip())
        colunas = linha_corrigida.split(',')

        nome_ator = colunas[0]
        try:
            num_filmes = int(float(colunas[2].strip()))  # Garantir conversão correta
            if num_filmes > max_num_filmes:
                ator_mais_filmes = nome_ator
                max_num_filmes = num_filmes
        except ValueError:
            print(f"[Atenção] Dados incorretos para {nome_ator}: {colunas[2]}")
            continue

    resultado = f"O ator/atriz com maior número de filmes é {ator_mais_filmes} com {max_num_filmes} filmes."
    with open("etapa1.txt", 'w', encoding='utf-8') as arquivo_saida:
        arquivo_saida.write(resultado)

    print(resultado)

etapa1()


def etapa2():
    with open("actors.csv", 'r', encoding='utf-8') as arquivo:
        linhas = arquivo.readlines()

    cabecalho = linhas[0]
    dados = linhas[1:]

    total_gross = 0
    num_registros = 0

    for linha in dados:
        linha_corrigida = re.sub(r'\"(.*?)\"', lambda x: x.group(0).replace(",", ""), linha.strip())
        colunas = linha_corrigida.split(',')

        try:
            gross = colunas[5].strip().replace(",", "")  # Coluna 'Gross'
            gross_value = float(gross)
            total_gross += gross_value
            num_registros += 1
        except ValueError:
            print(f"[Atenção] Dados incorretos na linha: {linha.strip()}")
            continue

    if num_registros > 0:
        media_gross = total_gross / num_registros
        resultado = f"A média de receita bruta dos principais filmes é: {media_gross:.2f} milhões de dólares."
    else:
        resultado = "Não foi possível calcular a média, pois não há registros válidos."

    with open("etapa2.txt", 'w', encoding='utf-8') as arquivo_saida:
        arquivo_saida.write(resultado)

    print(resultado)

etapa2()


def etapa_3():
    with open("actors.csv", 'r', encoding='utf-8') as arquivo:
        linhas = arquivo.readlines()

    # Remover o cabeçalho
    cabecalho = linhas[0]
    dados = linhas[1:]

    # Variáveis para encontrar a maior média de receita
    ator_maior_media = ""
    maior_media = 0

    for linha in dados:
        try:
            # Corrigir vírgulas dentro de aspas
            linha_corrigida = linha.strip().replace('"', '')
            colunas = linha_corrigida.split(',')

            # Extração das informações necessárias
            nome_ator = colunas[0].strip()  # Coluna 0: Nome do ator/atriz
            average_per_movie = colunas[3].strip()  # Coluna 3: Média de receita por filme

            # Limpeza e conversão do valor da média
            average_value = float(average_per_movie.replace(",", ""))

            # Comparação para encontrar a maior média
            if average_value > maior_media:
                maior_media = average_value
                ator_maior_media = nome_ator

        except ValueError:
            print(f"[Atenção] Dados incorretos na linha: {linha.strip()}")
            continue  # Ignorar linhas com valores inválidos

    # Gerar o resultado
    resultado = f"O ator/atriz com a maior média de receita bruta por filme é {ator_maior_media} com média de {maior_media:.2f} milhões de dólares por filme."

    # Salvar o resultado em etapa3.txt
    with open("etapa3.txt", 'w', encoding='utf-8') as arquivo_saida:
        arquivo_saida.write(resultado)

    # Feedback no console
    print(resultado)

# Chamada da função
etapa_3()


def etapa4():
    with open("actors.csv", 'r', encoding='utf-8') as arquivo:
        linhas = arquivo.readlines()

    # Remover o cabeçalho
    cabecalho = linhas[0]
    dados = linhas[1:]

    # Dicionário para armazenar a contagem de filmes
    contagem_filmes = {}

    # Processar cada linha do dataset
    for linha in dados:
        linha_corrigida = re.sub(r'\"(.*?)\"', lambda x: x.group(0).replace(",", ""), linha.strip())
        colunas = linha_corrigida.split(',')

        try:
            filme = colunas[4].strip()  # Coluna #1 Movie no índice 4

            # Contar as aparições do filme
            if filme in contagem_filmes:
                contagem_filmes[filme] += 1
            else:
                contagem_filmes[filme] = 1

        except IndexError:
            # Tratar linhas mal formatadas
            print(f"[Atenção] Linha incompleta ignorada: {linha.strip()}")
            continue

    # Ordenar os filmes por quantidade (decrescente) e depois pelo nome (crescente)
    filmes_ordenados = sorted(contagem_filmes.items(), key=lambda x: (-x[1], x[0]))

    # Gerar a saída formatada
    resultado = []
    for idx, (filme, quantidade) in enumerate(filmes_ordenados, start=1):
        resultado.append(f"({idx}) - O filme {filme} aparece ({quantidade}) vez(es) no dataset.")

    # Salvar o resultado no arquivo etapa4.txt
    with open("etapa4.txt", 'w', encoding='utf-8') as arquivo_saida:
        for linha in resultado:
            arquivo_saida.write(linha + "\n")

    # Imprimir o resultado no console
    for linha in resultado:
        print(linha)

# Chamada da função
etapa4()


def etapa5():
    with open("actors.csv", 'r', encoding='utf-8') as arquivo:
        linhas = arquivo.readlines()

    cabecalho = linhas[0]  # Pular cabeçalho
    dados = linhas[1:]

    receita_atores = []

    for linha in dados:
        try:
            # Substituir vírgulas dentro de aspas por '|'
            linha_corrigida = re.sub(r'\"(.*?)\"', lambda x: x.group(0).replace(',', '|'), linha.strip())

            # Dividir a linha em colunas
            colunas = linha_corrigida.split(',')

            # Restaurar as vírgulas substituídas por '|'
            colunas = [coluna.replace('|', ',').strip() for coluna in colunas]

            # Garantir que a linha tenha colunas suficientes
            if len(colunas) <= 2:
                continue

            # Extração de dados
            nome_ator = colunas[0]  # Coluna 0: Nome do ator
            total_gross = colunas[1]  # Coluna 2: Total Gross (na posição 1)

            # Conversão para float
            total_gross_value = float(total_gross)

            # Adicionar à lista
            receita_atores.append((nome_ator, total_gross_value))

        except (ValueError, IndexError) as e:
            print(f"[Atenção] Erro na linha: {linha.strip()} - {e}")
            continue  # Ignorar linhas inválidas

    # Ordenar pela receita total bruta em ordem decrescente
    receita_atores_ordenados = sorted(receita_atores, key=lambda x: -x[1])

    # Escrever no arquivo etapa5.txt
    with open("etapa5.txt", 'w', encoding='utf-8') as arquivo_saida:
        for nome, receita in receita_atores_ordenados:
            linha_saida = f"{nome} - {receita:.2f}"
            arquivo_saida.write(linha_saida + "\n")
            print(linha_saida)  # Imprimir no console

# Chamada da função
etapa5()
