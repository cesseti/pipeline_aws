# Resumo

**Noções básicas de Analytics na AWS – Parte 1 :** Conceitos básicos, como tipos de analytics, os 5 Vs do big data e os desafios associados ao processamento de grandes volumes de dados. Este curso também mapeia os 5 Vs do big data para os serviços de analytics da AWS e discute como a AWS fornece os serviços mais abrangentes do mercado.

**Fundamentos de analytics na AWS – Parte 2:**  Com base nos conceitos apresentados na Parte 1, este curso apresenta uma visão geral dos data lakes, data warehouses e das arquiteturas de dados modernas na AWS. Você aprenderá quais serviços da AWS podem ser usados para criar um data warehouse, data lakes e arquiteturas de dados modernas na AWS. Você também verá casos de uso comuns da arquitetura de dados moderna e uma arquitetura de referência. 

**Serverless Analytics:** Este curso mostrará como sintetizar todos esses diferentes dados usando o poder de ferramentas como AWS IoT Analytics, Amazon Cognito, AWS Lambda e Amazon SageMaker, entre outras.

**Introduction to Amazon Athena:** Este curso apresenta o serviço Amazon Athena junto com uma visão geral do ambiente operacional. Também são discutidas as etapas básicas da implementação do Amazon Athena. Usando o Console de Gerenciamento da AWS, é realizada uma breve demonstração da criação de um banco de dados para executar consultas SQL para validação.

**AWS Glue Getting Started:** Este curso ensina os benefícios, casos de uso típicos e conceitos técnicos do AWS Glue, incluindo o AWS Glue Studio e o AWS Glue DataBrew. O DataBrew é uma nova ferramenta de preparação de dados visuais que ajuda analistas e cientistas de dados a limpar e normalizar dados para prepará-los para análise e aprendizado de máquina.

**Amazon EMR Getting Started:** Este curso, ensina o Amazon EMR Serverless, que é uma nova opção no Amazon EMR que o torna eficiente e econômico para engenheiros e analistas de dados executarem aplicativos criados usando estruturas de big data de código aberto sem precisar ajustar, operar, otimizar, proteger ou gerenciar clusters. 

**Getting Started with Amazon Redshift:** Este curso, ensina os benefícios, os casos de uso mais comuns e os conceitos técnicos do Amazon Redshift.

**Best Practices for Data Warehousing with Amazon Redshift:** Este curso ensina sobre os conceitos de implementação de um data warehouse usando o Amazon Redshift.

**Amazon QuickSight - Getting Started:** Este curso ensina sobre os benefícios e conceitos técnicos do QuickSight.

# Exercícios

### Exercício 3 - Lab AWS Athena

[resultado](exercicios/athena/3-etapa_3.5-resultado.csv)

- [Exercício 3 - evidências](#exercício-3---lab-aws-athena-1)

### Exercício 4 - Lab AWS Lambda

[dockerfile](exercicios/lambda/dockerfile)

[minha-camada-pandas.zip](exercicios/lambda/minha-camada-pandas.zip)

- [Exercício 4 - evidências](#exercício-4---lab-aws-lambda-1)


# Evidências

## Exercício 3 - Lab AWS Athena

## Etapa 1: Configurar Athena
![Criar-Bucket](evidencias/exercicios/3-Athena/3-etapa_1.1-criar_bucket.png)

![bucket_criado](evidencias/exercicios/3-Athena/3-etapa_1.1-bucket_criado.png)

### upload csv
![upload](evidencias/exercicios/3-Athena/3-etapa_1.2-upload.png)

![upload](evidencias/exercicios/3-Athena/3-etapa_1.2-upload_feito.png)

### pasta queries
![queries](evidencias/exercicios/3-Athena/3-etapa_1.5-pasta_queries.png)

![queries](evidencias/exercicios/3-Athena/3-etapa_1.5-queries_criada.png)

### caminho para o bucket
![caminho para o bucket](evidencias/exercicios/3-Athena/3-etapa_1.9-caminho_pasta.png)

![caminho para o bucket](evidencias/exercicios/3-Athena/3-etapa_1.9-caminho%20salvo.png)


## Etapa 2: Criar um banco de dados
![criar_database](evidencias/exercicios/3-Athena/3-etapa_2-criar_database.png)


## Etapa 3: Criar uma tabela

### criar tabela 
![criar_tabela](evidencias/exercicios/3-Athena/3-etapa_3.1-criar_tabela.png)

![criar_tabela](evidencias/exercicios/3-Athena/3-etapa_3.1-sucesso.png)

### testando dados
![criar_tabela](evidencias/exercicios/3-Athena/3-etapa_3.4-testa_dados.png)

### resultado
![criar_tabela](evidencias/exercicios/3-Athena/3-etapa_3.4-resultado.png.png)

### consulta que lista os 3 nomes mais usados em cada década desde o 1950 até hoje.
``` sql
WITH decadas AS (
    SELECT 
        CAST(FLOOR(ano / 10) * 10 AS INTEGER) AS decada,
        nome,
        SUM(total) AS total_frequencia
    FROM cliente
    WHERE ano >= 1950
    GROUP BY CAST(FLOOR(ano / 10) * 10 AS INTEGER), nome
),
nomes_ranqueados AS (
    SELECT
        decada,
        nome,
        total_frequencia,
        ROW_NUMBER() OVER (PARTITION BY decada ORDER BY total_frequencia DESC) AS rank
    FROM decadas
)
SELECT
    decada,
    nome,
    total_frequencia
FROM nomes_ranqueados
WHERE rank <= 3
ORDER BY decada, rank;

```
### resultado: [query_final](exercicios/athena/3-etapa_3.5-resultado.csv)



## Exercício 4 - Lab AWS Lambda

## Etapa 1: Criar a função do Lambda
![criar_funcao](evidencias/exercicios/4-Lambda/4-e1-criar_funcao.png)


## Etapa 2: Construir o código

### criando teste
![criando-teste](evidencias/exercicios/4-Lambda/4-e2.3-criando-teste.png)

### erro
![erro](evidencias/exercicios/4-Lambda/4-e2.4-erro.png)


## Etapa3: Criar uma Layer

### dockerfile 
![dockerfile](evidencias/exercicios/4-Lambda/4-e3.1-dockerfile.png)

### imagem criada
![dockerfile](evidencias/exercicios/4-Lambda/4-e3.2-imagem_criada.png)

### diretorios criados
![diretorios](evidencias/exercicios/4-Lambda/4-e3.4-diretorios.png)

### baixando bibliotecas
![baixando bibliotecas](evidencias/exercicios/4-Lambda/4-e3.5-baixando_biblioteca.png)

### arquivos compactados
![compactado](evidencias/exercicios/4-Lambda/4-e3.7-compactado.png)

### copiar o zip do Container para a máquina local
![copiando_arquivo](evidencias/exercicios/4-Lambda/4-e3.8-copiando_arquivo.png)

### upload para o bucket
![arquivo_bucket](evidencias/exercicios/4-Lambda/4-e3.9-arquivo_bucket.png)

### criando camada 
![criando_camada](evidencias/exercicios/4-Lambda/4-e3.11-criando_camada.png)


## Etapa 4: Utilizando a Layer

### adicionando camada
![adicionando_camada](evidencias/exercicios/4-Lambda/4-e4.5-adicionando_camada.png)

### execução
![execucao](evidencias/exercicios/4-Lambda/4-e4.6-execucao.png)


# Certificados

[AWS Athena](./certificados/AWS%20Course%20Completion%20Certificate-athena.pdf)

[AWS Glue](./certificados/AWS%20Course%20Completion%20Certificate-Glue.pdf)

[AWS QuickSight](./certificados/AWS%20Course%20Completion%20Certificate-QuickSight.pdf)

[AWS Redshift](./certificados/AWS%20Course%20Completion%20Certificate-redshift.pdf)

[AWS Serveless Analytics](./certificados/AWS%20Course%20Completion%20Certificate-serveless_analytics.pdf)

[AWS Analytics Part 1](./certificados/AWS%20Skill%20Builder%20Course%20Completion%20Certificate-analytics-part1.pdf)

[AWS Analytics Part 2](./certificados/AWS%20Skill%20Builder%20Course%20Completion%20Certificate-analytics-part2.pdf)

[AWS Best Practicies](./certificados/AWS%20Skill%20Builder%20Course%20Completion%20Certificate-Best_Practicies.pdf)

[AWS EMR](./certificados/AWS%20Skill%20Builder%20Course%20Completion%20Certificate-EMR.pdf)
