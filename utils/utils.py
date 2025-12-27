import pandas as pd

# Função interna para converter colunas categóricas
def parse_categoricals(df: pd.DataFrame) -> pd.DataFrame:
    categorical_columns = [
        "Empresa Aérea",
        "Código Tipo Linha",
        "Aeródromo Origem",
        "Aeródromo Destino",
    ]
    for col in categorical_columns:
        df[col] = df[col].astype('category')
    
    return df

def parse_datetime(df: pd.DataFrame) -> pd.DataFrame:
    datetime_columns = [
        "Data Hora Voo",
    ]
    for col in datetime_columns:
        df[col] = pd.to_datetime(df[col], format="mixed", dayfirst=True, errors='coerce')
    
    return df