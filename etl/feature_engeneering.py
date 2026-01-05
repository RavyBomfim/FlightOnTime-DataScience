import pandas as pd
import numpy as np
     
def create_distance_col(df: pd.DataFrame, aerodromos: pd.DataFrame) -> pd.DataFrame:
    def merge_aerodromos(df: pd.DataFrame, tipo: str) -> pd.DataFrame:
        df = df.merge(
            aerodromos,
            left_on=f"Aeródromo {tipo.capitalize()}",
            right_on="Código OACI", 
            how='left'
        ).rename(columns={"Latitude": f"lat_{tipo}", "Longitude": f"lon_{tipo}"}).drop(columns="Código OACI")

        return df
    
    # Função interna para calcular a distância entre dois aeroportos
    def haversine(lat1, lon1, lat2, lon2):
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
    # Cria a coluna "Atrasado" com valores 0 e 1
    # 1 = Atrasado, 0 = No Horario
    df["Atrasado"] = (df["Partida Real"] > df["Partida Prevista"]).astype('int8')

    # Renomeia a coluna "Partida Prevista" para "Data Hora Voo"
    df = df.rename(columns={"Partida Prevista": "Data Hora Voo"})

    # Remove a coluna "Partida Real"
    df = df.drop(columns=["Partida Real"])

    return df

def clean_df(df: pd.DataFrame, aerodromos: pd.DataFrame, columns: list) -> pd.DataFrame:
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