import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType

## @params: [JOB_NAME, S3_INPUT_PATH, S3_TARGET_PATH]
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'S3_INPUT_PATH', 'S3_TARGET_PATH'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

input_path = args['S3_INPUT_PATH']
target_path = args['S3_TARGET_PATH']

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
df_paises = spark.read.option("multiLine", True).parquet(input_path + "part-00000-e25646d7-36a4-41d8-b07c-6158a2744179.c000.snappy.parquet")

window_spec_pais = Window.orderBy("codigo_pais")

dim_pais = df_paises.select(
    F.col("codigo_pais").alias("codigo_pais"),
    F.col("provedores").alias("plataforma")
).withColumn(
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

# Adicionar o ID de tempo (data_lancamento) ao DataFrame df_series
df_series_com_tempo = df_series.join(
    dim_tempo,
    df_series["dataLancamento"] == dim_tempo["data_lancamento"],
    "inner"
).select(
    df_series["*"]
)

# Criar a tabela de fatos
fato_series = df_series_com_tempo.join(
    df_personagens,
    df_series_com_tempo["numeroTemporada"] == df_personagens["numeroTemporada"],
    "inner"
).crossJoin(dim_pais).select(
    df_series_com_tempo["id"].alias("id_serie"),
    df_personagens["idArtista"].alias("id_personagem"),
    df_series_com_tempo["idTemporada"].alias("id_temporada"),
    dim_pais["id_pais"],
    df_series_com_tempo["dataLancamento"].alias("data_lancamento"),
    df_series_com_tempo["notaMedia"].alias("avaliacao"),
    df_series_com_tempo["popularidade"].alias("popularidade_serie"),
    df_personagens["popularidadeArtista"].alias("popularidade_personagem"),
    df_series_com_tempo["quantidadeTemporadas"].alias("numero_temporadas"),
    df_series_com_tempo["quantidadeEpisodios"].alias("numero_episodios"),
    df_series_com_tempo["numeroTemporada"].alias("numero_temporada"),
    df_personagens["ordemImportancia"].alias("ordem_importancia")
)


# Escrever como Parquet
fato_series.coalesce(1).write.mode("append").parquet(f"{target_path}/fato_series")

job.commit()