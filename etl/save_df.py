import os
import pandas as pd
from datetime import datetime

def save_df(df: pd.DataFrame, filename: str = "dados_voos", timestamp: bool = False, save_csv: bool = False) -> None:
    """
    Salva o DataFrame em formatos CSV e Parquet dentro do diretório root/data/.

    Parâmetros
    ----------
    df : pd.DataFrame
        - DataFrame que será salvo.
    filename : str, opcional
        - Nome base do arquivo (sem extensão). O padrão é "vra_master".
    timestamp : bool, opcional
        - Se True, adiciona ao nome do arquivo um sufixo com data e hora
        no formato YYYYMMDD_HHMMSS, garantindo unicidade e versionamento.

    Notas
    -----
    - O diretório ./data/ é criado automaticamente caso não exista.
    - Dois arquivos são gerados:
        • <filename>.csv (codificação UTF-8)  
        • <filename>.parquet (colunar, compactado)
    - O Parquet é recomendado para processamento posterior devido à maior velocidade
      de leitura e economia de memória.
    """

    # Garante que o diretório ./data/ exista
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    data_dir = os.path.abspath(data_dir)
    os.makedirs(data_dir, exist_ok=True)

    # Se timestamp=True, adiciona YYYYMMDD_HHMMSS ao nome do arquivo
    filename_raw = filename
    if timestamp:
        base, ext = os.path.splitext(filename)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{base}_{ts}{ext}"
        filename_raw = f"{base}_{ts}"

    # Caminho completo para salvar o arquivo
    filepath = os.path.join(data_dir, filename)

    # Salva o DataFrame em CSV
    if save_csv:
        df.to_csv(f'{filepath}.csv', index=False, encoding="utf-8")
        print(f"   → ./data/{filename_raw}.csv")
    
    # Salva o DataFrame em parquet
    print(f"📁 Arquivo salvo com sucesso:")
    df.to_parquet(f'{filepath}.parquet', engine="fastparquet", index=False)
    print(f"   → ./data/{filename_raw}.parquet")