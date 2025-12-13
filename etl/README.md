# ETL do Conjunto de Dados VRA (Voo Regular Ativo) – ANAC

**Arquivo:** `etl.py`  
**Formato final dos dados:** CSV e Parquet  
**Origem dos dados:** Portal de Dados Abertos da ANAC 

## Descrição

Este módulo implementa um pipeline de ETL (Extract, Transform, Load) para o conjunto **Voo Regular Ativo (VRA)**, disponibilizado pela **ANAC**.

Ele realiza automaticamente:

- **Geração das URLs** de todos os arquivos públicos do VRA (2000–2025).  
- **Download sequencial** dos CSVs diretamente da fonte.  
- **Limpeza, padronização e tipagem** dos dados.  
- **Conversão otimizada** de colunas categóricas e datas.  
- **Construção de um único DataFrame consolidado** contendo apenas voos **realizados**.  
- **Persistência** do resultado final em CSV e Parquet dentro de `root/data/`.

O objetivo é fornecer um dataset limpo, padronizado e eficiente para análises posteriores, incluindo modelagem, agregações, dashboards e aplicações externas.

## Estrutura do Arquivo

O arquivo `etl.py` contém três funções principais:

1. **`getUrls()`** → Gera dinamicamente todas as URLs oficiais dos CSVs do VRA.  
2. **`preprocess_csvs(urls)`** → Baixa, limpa, padroniza e consolida os dados.  
3. **`save_df(df, filename, timestamp)`** → Salva o resultado final em CSV e Parquet.

Cada função está documentada internamente com docstrings em português.

## Extração dos Dados

### Função: `getUrls()`

Gera a lista completa de URLs dos arquivos CSV do VRA, organizados por:

- Anos: **2000 a 2025**
- Meses: **Janeiro a Dezembro**
- Exclusão automática de meses > outubro/2025 (não disponíveis)

**Exemplo do formato das URLs:**

```
https://sistemas.anac.gov.br/.../2020/01 - Janeiro/VRA_202001.csv
```

**Retorno:**  
Lista com todas as URLs em ordem cronológica.

## Transformação dos Dados

### Função: `load_and_preprocess_csvs(urls)`

Para cada arquivo CSV, esta função:

1. **Lê** o arquivo bruto da ANAC.  
2. **Seleciona** apenas colunas relevantes.  
3. **Remove** voos cancelados.  
4. **Remove** linhas com datas ausentes.  
5. **Converte** datas para datetime.  
6. **Converte** colunas categóricas para category (otimiza memória em 70–90%).  
7. **Concatena** no DataFrame mestre.  
8. **Exibe** progresso, contagem de linhas e uso de memória.

**Retorno:**  
`pandas.DataFrame` consolidado com todos os voos **realizados**, pronto para uso.

## Carregamento dos Dados

### Função: `save_df(df, filename="vra_master", timestamp=False)`

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

## Inicialização

Para executar o ETL completo, dentro da pasta do projeto:

```bash
python etl/etl.py
```

## Exemplo de Uso (Código Python)

```python
from etl import getUrls, load_and_preprocess_csvs, save_df

# 1. Obter lista de URLs
urls = getUrls()

# 2. Baixar e preprocessar dados
df = load_and_preprocess_csvs(urls)

# 3. Salvar dataset final
save_df(df, filename="vra_dataset", timestamp=True)
```

## Exemplo de Saída

Ao final da execução, serão gerados arquivos como:

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

## Observações

- A execução completa pode levar tempo devido ao grande volume de arquivos (26 anos × 12 meses).
- O uso de `category` e Parquet reduz drasticamente o consumo de memória.
- Os CSVs originais podem conter milhões de registros; recomenda-se ter espaço suficiente em disco.
