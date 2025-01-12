import boto3

# guardando chamada de funcao em variavel
client = boto3.client('s3')

# criando bucket
client.create_bucket(Bucket = 'sprint05' )

# fazendo upload do arquivo original para o bucket
client.upload_file(Filename = 'InvestidoresTesouroDireto2018.csv',
                   Bucket = 'sprint05',
                   Key = 'InvestidoresTesouroDireto2018.csv')