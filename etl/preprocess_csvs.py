import pandas as pd
import numpy as np
from helpers.parsers import parse_categoricals, parse_datetime, parse_int
from etl.feature_engeneering import clean_df, create_distance_col, create_y_col

def preprocess_csvs(urls: list, aerodromos: pd.DataFrame) -> pd.DataFrame:
    """
    Carrega, filtra e preprocessa múltiplos arquivos CSV do VRA (Voo Regular Ativo) 
    disponibilizados pela ANAC, retornando um único DataFrame consolidado.

    Este procedimento realiza o download sequencial dos arquivos, aplica regras de ETL 
    para limpeza e normalização dos dados e concatena os resultados em um DataFrame único. 
    Ao final, os dados retornados contêm apenas informações relevantes para análise de 
    voos realizados, com colunas categóricas otimizadas e datas convertidas para datetime.

    Etapas executadas para cada arquivo CSV:
        1. Download e leitura do arquivo bruto, ignorando as duas primeiras linhas 
           (“Atualizado em” e o cabeçalho original).
        2. Seleção das colunas necessárias conforme o layout oficial da ANAC.
        3. Remoção de linhas cuja situação do voo seja "CANCELADO".
        4. Remoção de registros com valores ausentes nas colunas de data/hora.
        5. Conversão das colunas de data para o tipo datetime.
        6. Conversão de colunas categóricas para o tipo category (otimização de memória).
        7. Concatenação incremental no DataFrame mestre.

    Parâmetros
    ----------
    urls : list
        Lista contendo as URLs dos arquivos CSV a serem processados.
    aerodromos : pd.DataFrame
        DataFrame contendo informações sobre aeródromos da ANAC.

    Retorno
    -------
    pandas.DataFrame
        DataFrame consolidado contendo apenas voos realizados e colunas previamente 
        definidas, com tipagem otimizada e datas convertidas.

    Observações
    -----------
    - A função imprime estatísticas de progresso, quantidade de linhas carregadas 
      e uso de memória ao longo do processo.
    """

    print(f"Iniciando o download e preprocessamento de {len(urls)} arquivos CSV...\n")

    # Colunas do CSV original disponibilizado pela ANAC
    raw_columns = [
        "Empresa Aérea",
        "Número Voo",
        "Código Autorização (DI)",
        "Código Tipo Linha",
        "Aeródromo Origem",
        "Aeródromo Destino",
        "Partida Prevista",
        "Partida Real",
        "Chegada Prevista",
        "Chegada Real",
        "Situação Voo",
        "Código Justificativa"
    ]

    # Colunas desejadas
    columns = [
        "Empresa Aérea",
        "Aeródromo Origem",
        "Aeródromo Destino",
        "Partida Prevista",
        "Partida Real",
    ] 

    # Inicializa o DataFrame mestre
    master_df = pd.DataFrame()

    # Inicializa lista para armazenar DataFrames individuais
    dfs = []

    # Variáveis de controle
    lines = 0
    memory_usage = 0

    for i, url in enumerate(urls, start=1):

        print(f"[{i}/{len(urls)}] Carregando: {url.replace('https://sistemas.anac.gov.br/dadosabertos/Voos%20e%20opera%C3%A7%C3%B5es%20a%C3%A9reas/Voo%20Regular%20Ativo%20%28VRA%29', 'http://...')}")

        try:
            # Leitura do CSV bruto
            df = pd.read_csv(
                url,
                sep=';',
                quotechar='"',
                skiprows=2,         # pula "Atualizado em" + header
                header=None,
                names=raw_columns,
                low_memory=False
            )

        except Exception as e:
            print(f"❌ Falha ao ler {url}\nErro: {e}")
            continue

        if df.empty:
            print(f"⚠️ CSV vazio em {url}, ignorando.")
            continue

        # Limpeza de dados
        df = clean_df(df, aerodromos=aerodromos, columns=columns)

        # Engenharia de Features
        df = create_distance_col(df, aerodromos=aerodromos)
        df = create_y_col(df)

        # Parsing de tipos de dados
        df = parse_categoricals(df)
        df = parse_datetime(df)
        df = parse_int(df, col="Distância (m)", int_type='int32')

        # Adiciona o df limpo à lista
        dfs.append(df)

        lines += df.shape[0]
        memory_usage += df.memory_usage(deep=True).sum() / (1024 ** 2)
        print(f"✔ {df.shape[0]} linhas carregadas.")
        print(f"   Total atual de linhas: {lines}")
        print(f"   Memória usada: {memory_usage:.2f} MB\n")

    # Concatena todos os dfs ao DataFrame mestre
    master_df = pd.concat(dfs, ignore_index=True)

    print(f"\n🏁 Finalizado.\n")
    print(f"Total de linhas carregadas: {master_df.shape[0]}")
    print(f"Memória usada no Dataframe Master: {master_df.memory_usage(deep=True).sum() / (1024 ** 2):.2f} MB\n")

    return master_df