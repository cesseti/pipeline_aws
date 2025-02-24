import sys
import re
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType
import json
from pyspark.sql.functions import lit

## @params: [JOB_NAME, S3_INPUT_PATH, S3_TARGET_PATH]
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'S3_INPUT_PATH', 'S3_TARGET_PATH'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

input_path = args['S3_INPUT_PATH']
target_path = args['S3_TARGET_PATH']

# Pegar data de ingestão a partir do caminho 
match = re.search(r"/(\d{4})/(\d{2})/(\d{2})/$",input_path)
year, month, day = match.groups()

# Ler o arquivo dados_series.json
df_series = spark.read.option("multiLine", True).json(input_path + "dados_series.json")
# Adicionar colunas de partição
df_series = df_series.withColumn("ano", lit(year)).withColumn("mes", lit(month)).withColumn("dia", lit(day))
# Escrever como Parquet
df_series.write.mode("append").partitionBy("ano", "mes", "dia").parquet(target_path)

# Ler o arquivo dados_atores.json
df_atores = spark.read.option("multiLine", True).json(input_path + "dados_atores.json")
# Adicionar colunas de partição
df_atores = df_atores.withColumn("ano", lit(year)).withColumn("mes", lit(month)).withColumn("dia", lit(day))
# Escrever como Parquet
df_atores.write.mode("append").partitionBy("ano", "mes", "dia").parquet(target_path)

# Ler o arquivo dados_paises.json
df_paises = spark.read.option("multiLine", True).json(input_path + "dados_paises.json")
# Adicionar colunas de partição
df_paises = df_paises.withColumn("ano", lit(year)).withColumn("mes", lit(month)).withColumn("dia", lit(day))
# Escrever como Parquet
df_paises.write.mode("append").partitionBy("ano", "mes", "dia").parquet(target_path)

job.commit()