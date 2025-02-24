import sys
import re
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType
from pyspark.sql.functions import col, lit

## @params: [JOB_NAME, S3_INPUT_PATH_SINGLE, S3_INPUT_PATH_MULTI, S3_TARGET_PATH]
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

# Ler arquivo CSV original
df = spark.read.option("header", True).option("delimiter", "|").option("inferSchema", True).csv(input_path)

# Converter coluna "genero" para StringType
df = df.withColumn("genero", col("genero").cast(StringType()))

# Filtrar dados para séries de crime
df_crime = df.filter(col("genero").contains("Crime"))

# Adicionar colunas de partição
df_crime = df_crime.withColumn("ano", lit(year)).withColumn("mes", lit(month)).withColumn("dia", lit(day))

# Escrever como Parquet
df_crime.write.mode("append").partitionBy("ano", "mes", "dia").parquet(target_path)

job.commit()