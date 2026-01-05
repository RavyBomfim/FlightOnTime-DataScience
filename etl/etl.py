import os
import pandas as pd

from etl.save_df import save_df
from etl.get_urls import get_urls
from etl.preprocess_csvs import preprocess_csvs

from helpers.parsers import parse_categoricals, parse_datetime, parse_int


def processar_dados(save: bool = True) -> pd.DataFrame:
    """
    Executa o pipeline completo de ETL dos dados de voos a partir da base de dados de vôos da ANAC (Agência Nacional de Aviação Civil).

    Baixa os arquivos CSV brutos, realiza o pré-processamento, consolida os dados
    em um único DataFrame e salva automaticamente os resultados em formatos
    CSV e Parquet no diretório ./data/, com versionamento por timestamp.

    Parâmetros
    ----------
    **save** : bool, opcional
        Indica se o DataFrame resultante deve ser salvo em disco.
        Padrão é True, o que significa que os arquivos serão salvos
        automaticamente.

    Retorna
    -------
    pd.DataFrame
        Dataset consolidado e pré-processado.
    """
    urls = get_urls()
    aerodromos = pd.read_csv("metadata/aerodromos.csv")

    dataset = preprocess_csvs(urls, aerodromos)
    if save:
      save_df(dataset, timestamp=True)

    return dataset   


def carregar_dados(filename: str) -> pd.DataFrame:
    """
    Carrega um dataset de voos previamente pré-processado a partir de um arquivo Parquet
    e aplica conversões de tipo para colunas categóricas e de data/hora.

    Parâmetros
    ----------
    filename : str
        Nome-base do arquivo Parquet localizado em ./data/.
        Não inclua a extensão ".parquet".

    Retorna
    -------
    pd.DataFrame
        Dataset carregado com colunas categóricas convertidas para `category`
        e colunas de data/hora convertidas para `datetime`, pronto para análise
        ou modelagem.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    filepath = os.path.join(project_root, "data", f"{filename}.parquet")
    print(f"Carregando dataset local de: ./data/{filename}.parquet")

    dataset = pd.read_parquet(filepath)
    dataset = parse_categoricals(dataset)
    dataset = parse_datetime(dataset)
    dataset = parse_int(dataset, col="Distância (m)", int_type='int32')
    print("🏁 Dataset carregado com sucesso!")

    return dataset