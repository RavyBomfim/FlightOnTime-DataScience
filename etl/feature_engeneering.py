import pandas as pd
import numpy as np

def merge_aerodromos(df: pd.DataFrame, aerodromos: pd.DataFrame, tipo: str) -> pd.DataFrame:
    """
    Realiza o merge do DataFrame principal com a base de aeródromos,
    adicionando latitude e longitude conforme o tipo informado.

    Parâmetros
    ----------
    df : pandas.DataFrame
        - DataFrame principal contendo o código do aeródromo.
    tipo : str
        - Define se o merge será feito para origem ou destino.

    Retorna
    -------
    pandas.DataFrame
        - DataFrame com as colunas de latitude e longitude incorporadas.
    """
    df = df.merge(
        aerodromos,
        left_on=f"Aeródromo {tipo.capitalize()}",
        right_on="Código OACI", 
        how='left'
    ).rename(columns={"Latitude": f"lat_{tipo}", "Longitude": f"lon_{tipo}"}).drop(columns="Código OACI")

    return df

def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calcula a distância em linha reta entre dois pontos geográficos
    utilizando a fórmula de Haversine.

    Parâmetros
    ----------
    lat1, lon1 : float
        - Latitude e longitude do ponto de origem em graus.
    lat2, lon2 : float
        - Latitude e longitude do ponto de destino em graus.

    Retorna
    -------
    float
        - Distância aproximada entre os pontos, em metros.
    """
    R = 6371 # raio da terra em km

    # Converte as latitudes e longitudes de graus para radianos
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])

    # Diferença entre as latitudes dos dois pontos
    dlat = lat2 - lat1

    # Diferença entre as longitudes dos dois pontos
    dlon = lon2 - lon1

    # Obtém o valor intermediário que representa a separação angular entre os dois pontos
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2

    # Obtém o ângulo central entre os dois pontos na superfície da Terra
    c = 2 * np.arcsin(np.sqrt(a))

    # Arrendonda o resultado do cáculo em km e converte para metros
    distance = (round(R * c, 0) * 1000)

    return distance
     
def create_distance_col(df: pd.DataFrame) -> pd.DataFrame:
    """
    Insere as colunas de latitude e longitude para os aeróromos de origem e destino no DataFrame 
    de voos por meio da função merge_aerodromos, calcula a distância entre os aeródromos 
    de origem e destino utilizando a função haversine e, por fim, remove as colunas auxiliares 
    de latitude e longitude.

    Parâmetros
    ----------
    df : pandas.DataFrame
        - DataFrame contendo os dados de voos.

    Retorna
    -------
    pandas.DataFrame
        - DataFrame com a coluna "Distância (m)" inserida e colunas
        auxiliares removidas.
    """
    df = merge_aerodromos(df, "origem")
    df = merge_aerodromos(df, "destino")

    distances = haversine(
        df["lat_origem"],
        df["lon_origem"],
        df["lat_destino"],
        df["lon_destino"]
    )

    # Insere a coluna "Distância (km)" logo após a coluna "Aeródromo Destino"
    pos = df.columns.get_loc("Aeródromo Destino") + 1 # type: ignore
    df.insert(pos, "Distância (m)", distances) # type: ignore

    df = df.drop(columns=["lat_origem", "lon_origem", "lat_destino", "lon_destino"])

    return df

def create_y_col(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cria a variável alvo de atraso com valores 1 = Atrasado e 0 = No horário, 
    a partir dos horários de partida real e prevista e ajusta as colunas temporais
    do DataFrame de voos.

    Parâmetros
    ----------
    df : pandas.DataFrame
        - DataFrame contendo os dados de voos com horários previstos e reais.

    Retorna
    -------
    pandas.DataFrame
        - DataFrame com a coluna "Atrasado" criada, a coluna de data e hora
        renomeada e colunas auxiliares removidas.
    """
    df["Atrasado"] = (df["Partida Real"] > df["Partida Prevista"]).astype('int8')

    # Renomeia a coluna "Partida Prevista" para "Data Hora Voo"
    df = df.rename(columns={"Partida Prevista": "Data Hora Voo"})

    # Remove a coluna "Partida Real"
    df = df.drop(columns=["Partida Real"])

    return df

def clean_df(df: pd.DataFrame, aerodromos: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Realiza a limpeza e filtragem do DataFrame de voos conforme critérios
    específicos, incluindo a remoção de voos cancelados.

    Parâmetros
    ----------
    df : pandas.DataFrame
        - DataFrame contendo os dados brutos de voos.
    aerodromos : pandas.DataFrame
        - DataFrame com os aeródromos válidos, contendo o código OACI.
    columns : list
        - Lista de colunas a serem mantidas no DataFrame final.

    Retorna
    -------
    pandas.DataFrame
        - DataFrame de voos filtrado e contendo apenas as colunas
        especificadas.
    """
    # Remove voos cancelados
    df = df[df["Situação Voo"] == "REALIZADO"]

    # Remove os voos cujos "Aeródromo Origem" ou "Aeródromo Destino" não estejam na lista de aeródromos da ANAC 
    df = df[df["Aeródromo Origem"].isin(aerodromos["Código OACI"])]
    df = df[df["Aeródromo Destino"].isin(aerodromos["Código OACI"])]

    # Mantém apenas os voos regulares
    df = df[df["Código Autorização (DI)"] == "0"]

    # Filtra os tipos de linhas de voo
    df = df[df["Código Tipo Linha"].isin(["N", "R", "H"])]

    # Remove NaN das colunas "Partida Prevista" e "Partida Real"
    df = df.dropna(subset=["Partida Prevista", "Partida Real", "Código Tipo Linha"])

    # Mantém apenas as colunas desejadas
    df = df[columns]

    return df