import json
import pandas as pd
import boto3
import requests
import os
import io
from datetime import datetime

def lambda_handler(event, context):
    s3_client = boto3.client('s3')
    
    # Acessando arquivo
    bucket_name = 'data-lake-carlos'
    s3_file_name = 'Raw/Local/CSV/Movies/2025/01/27/movies.csv'
    objeto = s3_client.get_object(Bucket=bucket_name, Key=s3_file_name)

    # Lê o arquivo
    csv_content = objeto['Body'].read().decode('utf-8')

    # Usando IO para ler o arquivo como string e depois o pandas consegue ler como df
    df = pd.read_csv(io.StringIO(csv_content), sep='|', dtype={3: str})

    # Filtrando para meu gênero de filmes
    df_filtered = df[df['genero'] == 'War']

    # Tirando duplicatas e mantendo filmes únicos por ID
    df_filtered = df_filtered.drop_duplicates('id', keep= 'first')

    # Função que busca os dados por ID do filme
    def search_data(id_movie, api_key):
        url = f"https://api.themoviedb.org/3/movie/{id_movie}"
        params = {
            "api_key": api_key,
            "language": "pt-BR"  
        }

        response = requests.get(url, params=params) 

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Erro ao buscar filme com ID {id_movie}: {response.status_code}")
            return None

    # Chave api
    api_key = os.environ.get('API_KEY')

    # Lista para armazenar os dados
    data = []

    # For para passar id por id de todos os filmes na função
    for id_movie in df_filtered['id']:
        search = search_data(id_movie, api_key)

        if search:
            # For para pegar os países das produtoras que estão dentro de uma lista
            production_countries = [country['name'] for country in search.get('production_countries', [])]
            
            # Criando um dicionário para os dados de cada filme
            movie = {
                'id': id_movie,
                'receita': search.get('revenue', 'N/A'),
                'orcamento': search.get('budget', 'N/A'),
                'popularidade': search.get('popularity', 'N/A'),
                'paisFilme': search.get('origin_country', 'N/A'),
                'paisProdutora': ', '.join(production_countries)
            }
            data.append(movie)
        else:
            print(f"Nenhum dado encontrado para o filme com ID {id_movie}.")

    # Cria um DataFrame com os dados da api
    df_data = pd.DataFrame(data)
    print(f"Dados coletados: {len(df_data)} registros.")

    # Data para estruturar o caminho no S3
    current_date = datetime.now()
    year = current_date.strftime("%Y")
    month = current_date.strftime("%m")
    day = current_date.strftime("%d")

    # -- Dividindo os dados em JSONs com máximo de 100 registros cada --

    # Tamanho máximo de registros por arquivo
    max_length = 100

    # Calcula o número de partes necessárias
    num_parts = (len(df_data) // max_length) + (1 if len(df_data) % max_length != 0 else 0)
    print(f"Dividindo os dados em {num_parts} partes.")

    # Divide e salva cada parte em um arquivo JSON
    for i in range(num_parts):
        # Seleciona os registros da parte atual
        init = i * max_length
        end = (i + 1) * max_length
        part = df_data.iloc[init:end]

        # Salva a parte em um arquivo JSON
        file_name = f'Raw/TMDB/JSON/{year}/{month}/{day}/dados_filmes_parte_{i + 1}.json'
        file_content = part.to_json(orient='records', force_ascii=False, indent=4)
        print(f"Arquivo salvo: {file_name} (registros {init + 1} a {end})")

        # Envia o json para o S3
        try:
            s3_client.put_object(
                Bucket=bucket_name,
                Key=file_name,
                Body=file_content
            )
            print(f"Arquivo {file_name} enviado com sucesso para o bucket {bucket_name}.")
        except Exception as e:
            print(f"Erro ao fazer upload do arquivo: {file_name} - Erro: {e}")

    return {
        'statusCode': 200,
        'body': 'Processamento concluído!'
    }