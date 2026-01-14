import pandas as pd

def parse_categoricals(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converte colunas categóricas do DataFrame para o tipo category.

    Parâmetros
    ----------
    df : pandas.DataFrame
        - DataFrame contendo os dados a serem tipados.

    Retorna
    -------
    pandas.DataFrame
        - DataFrame com as colunas categóricas convertidas.
    """
    categorical_columns = [
        "Empresa Aérea",
        "Aeródromo Origem",
        "Aeródromo Destino",
    ]
    for col in categorical_columns:
        df[col] = df[col].astype('category')
    
    return df

def parse_datetime(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converte colunas de data e hora do DataFrame para o tipo datetime.

    Parâmetros
    ----------
    df : pandas.DataFrame
        - DataFrame contendo colunas temporais a serem convertidas.

    Retorna
    -------
    pandas.DataFrame
        - DataFrame com as colunas de data e hora convertidas.
    """
    datetime_columns = [
        "Data Hora Voo",
    ]
    for col in datetime_columns:
        df[col] = pd.to_datetime(df[col], format="mixed", dayfirst=True, errors='coerce')
    
    return df

def parse_int(df: pd.DataFrame, col: str, int_type: str = 'int32') -> pd.DataFrame:
    """
    Converte uma coluna do DataFrame para um tipo inteiro específico.

    Parâmetros
    ----------
    df : pandas.DataFrame
        - DataFrame contendo a coluna a ser convertida.
    col : str
        - Nome da coluna a ser convertida.
    int_type : str, opcional
        - Tipo inteiro de destino.

    Retorna
    -------
    pandas.DataFrame
        - DataFrame com a coluna convertida para o tipo inteiro definido.
    """
    df[col] = df[col].astype(int_type) # type: ignore
    return df