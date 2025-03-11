import json
import boto3
import requests
import os
from datetime import datetime


def lambda_handler(event, context):
    s3_client = boto3.client('s3')

    # Nome do bucket
    bucket_name = 'data-lake-carlos'
    
    # Função que busca os países de uma série
    def get_countries(series_id, api_key):
        url = f"https://api.themoviedb.org/3/tv/{series_id}/watch/providers"
        params = {
            "api_key": api_key
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Erro ao buscar provedores: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {e}")
            return None

    # Processa os dados dos países
    def process_country_data(country_data, series_id):
        results = []
        if "results" in country_data:
            for country_code, details in country_data["results"].items():
                providers_list = [p["provider_name"] for p in details.get("flatrate", [])]
                providers_str = ", ".join(providers_list) if providers_list else "Nenhum"
                # Adiciona um dicionário (objeto JSON) para cada país
                results.append({
                    "id_serie": series_id,  # Alterado para "id_serie"
                    "codigo_pais": country_code,
                    "provedores": providers_str
                })
        return results


    # Chave API
    api_key = os.environ.get('API_KEY')

    # ID da série Breaking Bad no TMDb
    series_id = 1396

    # Buscar os países
    countries_data = get_countries(series_id, api_key)

    # Processa os dados
    countries_list = process_country_data(countries_data, series_id)

    # Data para estruturar o caminho no S3
    current_date = datetime.now()
    year = current_date.strftime("%Y")
    month = current_date.strftime("%m")
    day = current_date.strftime("%d")

    # Salva os dados em JSON
    file_content = json.dumps(countries_list, ensure_ascii=False, indent=4)
    file_name = f'Raw/TMDB/JSON/{year}/{month}/{day}/dados_paises.json'

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