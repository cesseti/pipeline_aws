# Resumo

**AWS Cloud Quest:** O jogo da plataforma foi muito bom e intuitivo para aprender na prática os conceitos e serviços.

**AWS Preparatório:** O curso de preparação para a prova foi muito bom pois relembra muitos assuntos e nos ensina a ler e interpretar as questões da prova.

# Exercícios

### Exercício 3 - Lab AWS Athena

[resultado](exercicios/3-etapa_3.5-resultado.csv)

# Evidências

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
### resultado: [query_final](exercicios/3-etapa_3.5-resultado.csv)

# Certificados

[AWS Skill Builder](./certificados/18719_5_6675764_1736804772_AWS%20Skill%20Builder%20Course%20Completion%20Certificate.pdf)

[AWS Cloud Quest](https://www.credly.com/badges/e107cd36-0ba2-451d-9efc-48d5c1341ae0/public_url)
