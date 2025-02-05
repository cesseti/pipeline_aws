import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import functions as F
from awsglue.dynamicframe import DynamicFrame

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'S3_INPUT_PATH', 'S3_TARGET_PATH'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

source_file = args['S3_INPUT_PATH']
target_path = args['S3_TARGET_PATH']

# Ler o arquivo nomes.csv no S3
df = glueContext.create_dynamic_frame.from_options(
    "s3",
    {"paths": [source_file]},
    "csv",
    {"withHeader": True, "separator": ","}
)

# Exibir schema antes da conversão
df.printSchema()

# Convertendo para dataFrame spark
spark_df = df.toDF()

# Exibir as primeiras linhas do DataFrame
spark_df.show()

# Imprimir o schema do dataframe gerado no passo anterior
spark_df.printSchema()

# alterar a caixa dos valores da coluna nome para MAIÚSCULO
spark_df = spark_df.withColumn("nome", F.upper(F.col("nome")))

# Imprimir a contagem de nomes, agrupando os dados do dataframe pelas colunas ano e sexo. Ordene os dados de modo que o ano mais recente apareça como primeiro registro do dataframe
spark_df.groupBy("ano", "sexo").agg(F.sum("total").alias("total")).orderBy(F.col("ano").desc()).show()

# Apresentar qual foi o nome feminino com mais registros e em que ano ocorreu
spark_df.filter(F.col("sexo") == "F").groupBy("nome", "ano").agg(F.sum("total").alias("total")).orderBy(F.desc("total")).limit(1).show()

# Apresentar qual foi o nome masculino com mais registros e em que ano ocorreu
spark_df.filter(F.col("sexo") == "M").groupBy("nome", "ano").agg(F.sum("total").alias("total")).orderBy(F.desc("total")).limit(1).show()

# Apresentar o total de registros (masculinos e femininos) para cada ano presente no dataframe. Considere apenas as primeiras 10 linhas, ordenadas pelo ano, de forma crescente. 
spark_df.groupBy("ano").agg(F.sum("total").alias("total")).orderBy("ano").limit(10).show()

# Retornando ao frame dinamico
dynamic_upper_df = DynamicFrame.fromDF(spark_df, glueContext)

# Escrever o conteúdo do dataframe com os valores de nome em maiúsculo no S3
glueContext.write_dynamic_frame.from_options(
    frame = dynamic_upper_df ,
    connection_type = 's3' , 
    connection_options = {
        "path": target_path,
        "partitionKeys": ["sexo", "ano"]
    }, 
    format = "json"
    )

job.commit()