import boto3 
import pandas as pd
from datetime import datetime

# guardando chamada de funcao em variavel
client = boto3.client('s3')

# criando bucket
try:
    client.create_bucket(Bucket = 'data-lake-carlos' )
    print ("Bucket criado com sucesso")
except Exception as e:
    print (f"Erro ao criar bucket: {e}")

# diretório onde os arquivos estarão no container
data_dir = "./data"

# lendo os datasets
df_m = pd.read_csv(f"{data_dir}/movies.csv", sep='|', dtype={3: str})
df_s = pd.read_csv(f"{data_dir}/series.csv", sep='|', dtype={3: str})

# data para estruturar o caminho no S3
current_date = datetime.now()
year = current_date.strftime("%Y")
month = current_date.strftime("%m")
day = current_date.strftime("%d")

# fazendo upload dos arquivos para nuvem
bucket_name = "data-lake-carlos"

try:
    client.upload_file(
        Filename=f"{data_dir}/movies.csv",
        Bucket=bucket_name,
        Key=f"Raw/Local/CSV/Movies/{year}/{month}/{day}/movies.csv"
    )
    print("Upload de 'movies.csv' concluído!")
except Exception as e:
    print(f"Erro ao fazer upload de 'movies.csv': {e}")

try:
    client.upload_file(
        Filename=f"{data_dir}/series.csv",
        Bucket=bucket_name,
        Key=f"Raw/Local/CSV/Series/{year}/{month}/{day}/series.csv"
    )
    print("Upload de 'series.csv' concluído!")
except Exception as e:
    print(f"Erro ao fazer upload de 'series.csv': {e}")
