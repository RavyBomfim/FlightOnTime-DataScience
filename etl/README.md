# ETL do Conjunto de Dados VRA (Voo Regular Ativo) – ANAC

**Arquivo Principal:** `etl.py`  
**Formato final dos dados:** CSV e Parquet  
**Origem dos dados:** Portal de Dados Abertos da ANAC 

## Descrição

Este módulo implementa um pipeline de ETL (Extract, Transform, Load) para o conjunto **Voo Regular Ativo (VRA)**, disponibilizado pela **ANAC**.

Ele realiza automaticamente:

- **Geração das URLs** de todos os arquivos públicos do VRA (2000–2025).  
- **Download sequencial** dos CSVs diretamente da fonte.  
- **Limpeza, padronização e tipagem** dos dados.  
- **Conversão otimizada** de colunas categóricas, valores numéricos e datas.  
- **Engenharia de Features** para geração de colunas otimizadas para Machine Learning.  
- **Construção de um único DataFrame consolidado** contendo apenas voos **realizados**.  
- **Persistência** do resultado final em CSV e Parquet dentro de `root/data/`.

O objetivo é fornecer um dataset limpo, padronizado e eficiente para análises posteriores, incluindo modelagem, agregações, dashboards e aplicações externas.

## Estrutura do Módulo

O módulo `etl` contém três funções principais:

1. **`get_urls()`** → Gera dinamicamente todas as URLs oficiais dos CSVs do VRA.  
2. **`preprocess_csvs(urls)`** → Baixa, limpa, padroniza, transforma e consolida os dados.  
3. **`save_df(df, filename, timestamp)`** → Salva o resultado final em CSV e Parquet.

Cada função está documentada internamente com docstrings em português.

## Arquivo Principal

O arquivo `etl.py` abstrai o processo em duas funções:  

1. **`processar_dados()`** → Executa o pipeline completo, salva (opcional) e retorna o dataframe consolidado.  
2. **`carregar_dados()`** → Carrega os dados de um arquivo .parquet salvo previamente.  

## Extração dos Dados

### Arquivo: `get_urls.py`

Gera a lista completa de URLs dos arquivos CSV do VRA, organizados por:

- Anos: **2018 a 2025**
- Meses: **Janeiro a Dezembro**
- Exclusão automática de meses > outubro/2025 (não disponíveis)

**Exemplo do formato das URLs:**

```
https://sistemas.anac.gov.br/.../2020/01 - Janeiro/VRA_202001.csv
```

**Retorno:**  
Lista com todas as URLs em ordem cronológica.

## Transformação dos Dados

### Arquivo: `preprocess_csvs.py`

Para cada arquivo CSV, esta função:

1. **Lê** o arquivo bruto da ANAC.  
2. **Seleciona** apenas colunas relevantes.  
3. **Remove** voos cancelados.  
4. **Remove** voos cujos "Aeródromo Origem" ou "Aeródromo Destino" não estejam na lista de aeródromos da ANAC.  
5. **Remove** voos não-regulares.  
6. **Filtra** tipos de linhas de voo.  
7. **Remove** linhas com dados nulos.  
8. **Converte** datas para datetime.  
9. **Converte** colunas categóricas para category (otimiza memória em 70–90%).  
10. **Gera** coluna Y de vôos atrasados e coluna "Distância (m)" entre aeródromos.  
11. **Concatena** no DataFrame mestre.  
12. **Exibe** progresso, contagem de linhas e uso de memória.

**Retorno:**  
`pandas.DataFrame` consolidado, pronto para uso em Machine Learning.

## Carregamento dos Dados

### Arquivo: `save_df.py`

Salva o DataFrame final em dois formatos:

| Formato   | Características |
|-----------|-----------------|
| **CSV**   | Compatível com qualquer ferramenta, simples, UTF-8 |
| **Parquet** | Formato colunar, muito mais rápido e leve para processamento |

Os arquivos são salvos automaticamente em:

```
root/data/
```

Se `timestamp=True`, o nome do arquivo receberá um sufixo no formato:

```
vra_master_20250210_145233.csv
vra_master_20250210_145233.parquet
```

## Exemplo de Saída

Ao final da execução do ETL, serão gerados arquivos como:

```
root/data/vra_dataset.csv
root/data/vra_dataset.parquet
```

E o console exibirá mensagens como:

```
[89/312] Carregando: .../VRA_200112.csv
✔ 52.391 linhas carregadas.
   Total atual de linhas: 1.147.820
   Memória usada: 23.41 MB
```

## Exemplos de Uso (Código Python)

Realizar ETL completo:  

```python
from etl.etl import processar_dados

df = processar_dados()
```

Carregar dados previamente processados:  

```python
from etl.etl import carregar_dados

filename = "dados_voos_20260103_220419"
df = carregar_dados(filename=filename)
```

## Observações

- A execução completa pode levar tempo devido ao grande volume de arquivos (7 anos × 12 meses + 1 ano × 10 meses).
- O uso de `category`, `datetime`, dimensionamento adequado de `int` e Parquet reduz drasticamente o consumo de memória.
- Os CSVs originais podem conter milhões de registros; recomenda-se ter espaço suficiente em disco.
