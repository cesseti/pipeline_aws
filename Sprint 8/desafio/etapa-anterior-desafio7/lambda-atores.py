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

   # busca os créditos da temporada
    def get_season_credits(series_id, season_number, api_key):
        url = f"https://api.themoviedb.org/3/tv/{series_id}/season/{season_number}/credits"
        params = {
            "api_key": api_key,
            "language": "pt-BR"
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Erro ao buscar temporada {season_number}: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {e}")
            return None

    # pega os dados dos personagens
    def process_character_data(credits, series_id, season_number):
        characters = []
        for actor in credits.get('cast', []):
            character = {
                'id': series_id,
                'numeroTemporada': season_number,
                'idArtista': actor.get('id', 'N/A'),
                'artista': actor.get('name', 'N/A'),
                'personagem': actor.get('character', 'N/A'),
                'genero': actor.get('gender', 'N/A'),
                'ordemImportancia': actor.get('order', 'N/A'),
                'popularidadeArtista': actor.get('popularity', 'N/A')
            }
            characters.append(character)
        return characters

    # Chave api
    api_key = os.environ.get('API_KEY')

    # id da série Breaking Bad no TMDb
    series_id = 1396

    # Número de temporadas
    num_temporadas = 5

    # lista para armazenar os dados dos personagens
    all_characters = []

    # for que busca os dados de cada temporada
    for season in range(1, num_temporadas + 1):
        print(f"Buscando dados da temporada {season}...")
        credits = get_season_credits(series_id, season, api_key)
        if credits:
            characters = process_character_data(credits, series_id, season)
            all_characters.extend(characters)
        else:
            print(f"Nenhum dado encontrado para a temporada {season}.")

    # Cria um DataFrame com os dados dos personagens
    df_characters = pd.DataFrame(all_characters)

    # Data para estruturar o caminho no S3
    current_date = datetime.now()
    year = current_date.strftime("%Y")
    month = current_date.strftime("%m")
    day = current_date.strftime("%d")


    # Salva a parte em um arquivo JSON
    file_name = f'Raw/TMDB/JSON/{year}/{month}/{day}/dados_atores.json'
    file_content = df_characters.to_json(orient='records', force_ascii=False, indent=4)
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