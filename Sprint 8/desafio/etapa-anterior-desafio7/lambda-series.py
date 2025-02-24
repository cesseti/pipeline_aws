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
    s3_file_name = 'Raw/Local/CSV/Series/2025/01/27/series.csv'
    objeto = s3_client.get_object(Bucket=bucket_name, Key=s3_file_name)

    # Lê o arquivo
    csv_content = objeto['Body'].read().decode('utf-8')

    # Usando IO para ler o arquivo como string e depois o pandas consegue ler como df
    df = pd.read_csv(io.StringIO(csv_content), sep='|', dtype={3: str})

    # filtrando dados a serem buscados
    df_crime = df[df['genero'].str.contains('Crime', na=False)]
    df_crime = df_crime.drop_duplicates('id', keep='first')
    df_crime_top_rated = df_crime[df_crime['numeroVotos'] > 500000]

    # dicionário que armazena o id do tmdb
    id_mapping = {} 

    # função que busca o ID do TMDb a partir do IMDb ID
    def get_tmdb_id(imdb_id, api_key):
        url = f"https://api.themoviedb.org/3/find/{imdb_id}"
        params = {
            "api_key": api_key,
            "external_source": "imdb_id"
        }

        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if "tv_results" in data and data["tv_results"]:
                return data["tv_results"][0]["id"]
            else:
                print(f"Nenhuma série encontrada para IMDb ID {imdb_id}")
                return None
        else:
            print(f"Erro ao buscar IMDb ID {imdb_id}: {response.status_code}")
            return None

    # Função que busca os dados por ID da serie
    def search_series_data(id_series, api_key):
        url = f"https://api.themoviedb.org/3/tv/{id_series}"
        params = {
            "api_key": api_key,
            "language": "pt-BR",
            "append_to_response": "seasons" 
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Erro ao buscar série com ID {id_series}: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {e}")
            return None

    # Chave api
    api_key = os.environ.get('API_KEY')

    # Lista para armazenar os dados
    merged_data = []

    # for para buscar id por id do imdb
    for imdb_id in df_crime_top_rated['id']:
        tmdb_id = get_tmdb_id(imdb_id, api_key)
    
        id_mapping[imdb_id] = tmdb_id

    # For para passar ID por ID de todas as séries na função
    for imdb_id, tmdb_id in id_mapping.items():
        search = search_series_data(tmdb_id, api_key)

        if search:
            # dados gerais da série
            series_info = {
                'id': imdb_id,
                'titulo': search.get('name', 'N/A'),
                'popularidade': search.get('popularity', 'N/A'),
                'paisOrigem': ', '.join(search.get('origin_country', [])),
                'quantidadeTemporadas': search.get('number_of_seasons', 'N/A'),
                'quantidadeEpisodios': search.get('number_of_episodes', 'N/A')
            }

            # dados de temporada por temporada
            if "seasons" in search:
                for season in search["seasons"]:
                    season_info = {
                        'id': imdb_id,
                        'idTemporada': season.get('id', 'N/A'),
                        'tituloTemporada': season.get('name', 'N/A'),
                        'numeroTemporada': season.get('season_number', 'N/A'),
                        'dataLancamento': season.get('air_date', 'N/A'),
                        'notaMedia': season.get('vote_average', 'N/A'),
                        'totalVotos': season.get('vote_count', 'N/A')
                    }
                    # junta todos os dados
                    merged_data.append({**series_info, **season_info})

    # cria DataFrame com dados da api
    df_final = pd.DataFrame(merged_data)

    print(f"Dados coletados: {len(df_final)} registros.")

    # Data para estruturar o caminho no S3
    current_date = datetime.now()
    year = current_date.strftime("%Y")
    month = current_date.strftime("%m")
    day = current_date.strftime("%d")


    # Salva a parte em um arquivo JSON
    file_name = f'Raw/TMDB/JSON/{year}/{month}/{day}/dados_series.json'
    file_content = df_final.to_json(orient='records', force_ascii=False, indent=4)
    print(f"Arquivo salvo: {file_name}")

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