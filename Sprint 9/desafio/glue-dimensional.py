import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType
from pyspark.sql.window import Window
from pyspark.sql.functions import row_number

## @params: [JOB_NAME, S3_INPUT_PATH, S3_TARGET_PATH]
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'S3_INPUT_PATH', 'S3_INPUT_COUNTRY', 'S3_TARGET_PATH'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

input_path = args['S3_INPUT_PATH']
target_path = args['S3_TARGET_PATH']
input_country = args['S3_INPUT_COUNTRY']

# Ler o arquivo de series
df_series = spark.read.option("multiLine", True).parquet(input_path + "part-00000-d52a74e9-3184-49a9-a54d-2c4fd0b0549a.c000.snappy.parquet")

# Criar a dimensão série
dim_serie = df_series.select(
    F.col("id").alias("id_serie"),
    F.col("titulo").alias("titulo_serie"),
    F.col("paisOrigem").alias("codigo_pais")
)

# Escrever como Parquet
dim_serie.coalesce(1).write.mode("append").parquet(f"{target_path}/dim_serie")

# Ler o arquivo de personagens
df_personagens = spark.read.option("multiLine", True).parquet(input_path + "part-00000-2c29e18d-9441-45d3-ac02-05a53428aac6.c000.snappy.parquet")

# Criar a dimensão personagem
dim_personagem = df_personagens.select(
    F.col("idArtista").alias("id_personagem"),
    F.col("personagem").alias("nome_personagem"),
    F.col("artista").alias("nome_artista")
)

# Escrever como Parquet
dim_personagem.coalesce(1).write.mode("append").parquet(f"{target_path}/dim_personagem")


# Ler o arquivo de paises 
df_paises = spark.read.option("multiLine", True).parquet(input_country + "part-00000-1eb3a45e-f79c-4aff-9699-e651dfd20580.c000.snappy.parquet")

dim_pais = df_paises.select(
    F.col("id_serie"),
    F.col("codigo_pais").alias("codigo_pais"),
    F.col("provedores").alias("plataforma")
).distinct().withColumn(
    "id_pais", F.monotonically_increasing_id() # Criar IDs únicos para cada país
)

# Escrever como Parquet
dim_pais.coalesce(1).write.mode("append").parquet(f"{target_path}/dim_pais")


# Criar a dimensão tempo
dim_tempo = df_series.select(
    F.col("dataLancamento").alias("data_lancamento")
).distinct().withColumn(
    "ano", F.year("data_lancamento")
).withColumn(
    "mes", F.month("data_lancamento")
).select(
    "data_lancamento", "ano", "mes"
)

# Escrever como Parquet
dim_tempo = dim_tempo.repartition("ano", "mes")
dim_tempo.write.mode("append").partitionBy("ano", "mes").parquet(f"{target_path}/dim_tempo")


# Tabela Fatos

# Cria DF intermediario entre personagens e series para obter os IDs diferentes
df_series_personagens = df_personagens.join(
    df_series,
    df_personagens["numeroTemporada"] == df_series["numeroTemporada"],
    "inner"
).select(
    df_series["id"].alias("id_tmdb"),
    df_personagens["id"].alias("id_imdb")
)

# Criar um DataFrame que associa as séries aos países
df_series_paises = df_series_personagens.join(
    dim_pais,
    df_series_personagens["id_imdb"] == dim_pais["id_serie"],
    "left"
).select(
    df_series_personagens["id_tmdb"].alias("id_serie"),
    dim_pais["id_pais"]
)

# Adicionar o ID da tempo (data_lancamento) ao DataFrame df_series
df_series_com_tempo = df_series.join(
    dim_tempo,
    df_series["dataLancamento"] == dim_tempo["data_lancamento"],
    "inner"
).select(
    df_series["*"]
)


# Juntar os dados de séries e países
df_series_com_pais = df_series_com_tempo.join(
    df_series_paises,
    df_series_com_tempo["id"] == df_series_paises["id_serie"],
    "left"
).select(
    df_series_com_tempo["*"],
    df_series_paises["id_pais"]
)


# Criar tabela Fatos
fato_series = df_series_com_pais.join(
    df_personagens,
    df_series_com_pais["numeroTemporada"] == df_personagens["numeroTemporada"],
    "inner"
).select(
    df_series_com_pais["id"].alias("id_serie"),
    df_personagens["idArtista"].alias("id_personagem"),
    df_series_com_pais["idTemporada"].alias("id_temporada"),
    df_series_com_pais["id_pais"],
    df_series_com_pais["dataLancamento"].alias("data_lancamento"),
    df_series_com_pais["notaMedia"].alias("avaliacao"),
    df_series_com_pais["popularidade"].alias("popularidade_serie"),
    df_personagens["popularidadeArtista"].alias("popularidade_personagem"),
    df_series_com_pais["quantidadeTemporadas"].alias("numero_temporadas"),
    df_series_com_pais["quantidadeEpisodios"].alias("numero_episodios"),
    df_series_com_pais["numeroTemporada"].alias("numero_temporada"),
    df_personagens["ordemImportancia"].alias("ordem_importancia")
)


# Escrever como Parquet
fato_series.coalesce(1).write.mode("append").parquet(f"{target_path}/fato_series")

job.commit()