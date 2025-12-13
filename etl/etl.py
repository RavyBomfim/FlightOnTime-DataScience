import os
import pandas as pd
from datetime import datetime

def getUrls() -> list:
    """
    Gera a lista completa de URLs dos arquivos CSV do conjunto 
    “Voo Regular Ativo (VRA)” disponibilizado pela ANAC.

    A função constrói dinamicamente os caminhos de acesso aos arquivos 
    organizados por ano e mês, conforme a estrutura oficial do portal de 
    dados abertos da ANAC. São consideradas todas as combinações entre os anos 
    de 2000 a 2025 e os 12 meses do ano, com exceção dos meses posteriores a 
    outubro de 2025, pois esses arquivos ainda não estão disponíveis.

    Para cada combinação válida, é gerada a URL correspondente no formato:
        https://.../ANO/MM - Mês/VRA_ANOMM.csv

    Retorna uma lista contendo todas as URLs resultantes, na ordem cronológica.

    Retorno
    -------
    list
        Lista de strings contendo as URLs completas dos arquivos CSV do VRA.
    """

    url_base = "https://sistemas.anac.gov.br/dadosabertos/Voos%20e%20opera%C3%A7%C3%B5es%20a%C3%A9reas/Voo%20Regular%20Ativo%20%28VRA%29"
    anos = list(range(2000, 2026))
    meses = {
        1:  "01%20-%20Janeiro",
        2:  "02%20-%20Fevereiro",
        3:  "03%20-%20Mar%C3%A7o",
        4:  "04%20-%20Abril",
        5:  "05%20-%20Maio",
        6:  "06%20-%20Junho",
        7:  "07%20-%20Julho",
        8:  "08%20-%20Agosto",
        9:  "09%20-%20Setembro",
        10: "10%20-%20Outubro",
        11: "11%20-%20Novembro",
        12: "12%20-%20Dezembro"
    }

    urls = []

    for ano in anos:
        for mes in meses.items():
            if ano == 2025 and mes[0] > 10:
                continue
            url = f"{url_base}/{ano}/{mes[1]}/VRA_{ano}{mes[0]}.csv"
            urls.append(url)
    
    return urls


def preprocess_csvs(urls: list) -> pd.DataFrame:
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

    # Função interna para limpeza do DataFrame
    def clean_df(df: pd.DataFrame, columns: list) -> pd.DataFrame:
        # Remove voos cancelados
        df = df[df["Situação Voo"] == "REALIZADO"]

        # Remove NaN das colunas "Partida Prevista" e "Partida Real"
        df = df.dropna(subset=["Partida Prevista", "Partida Real"])

        # Mantém apenas as colunas desejadas
        df = df[columns]

        return df
    
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
    
    # Função interna para converter colunas de data/hora
    def parse_datetime(df: pd.DataFrame) -> pd.DataFrame:
        datetime_columns = [
            "Partida Prevista",
            "Partida Real",
        ]
        for col in datetime_columns:
            df[col] = pd.to_datetime(df[col], format="mixed", dayfirst=True, errors='coerce')
        
        return df
    
    # Colunas finais desejadas
    columns = [
        "Empresa Aérea",
        "Código Tipo Linha",
        "Aeródromo Origem",
        "Aeródromo Destino",
        "Partida Prevista",
        "Partida Real",
    ]

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

    # Inicializa o DataFrame mestre apenas com as colunas desejadas
    master_df = pd.DataFrame(columns=columns)

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

        # Limpeza e parseamento
        df = clean_df(df, columns)
        df = parse_categoricals(df)
        df = parse_datetime(df)

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


def save_df(df: pd.DataFrame, filename: str = "vra_master", timestamp: bool = False) -> None:
    """
    Salva o DataFrame em formatos CSV e Parquet dentro do diretório root/data/.

    Parâmetros
    ----------
    df : pd.DataFrame
        DataFrame que será salvo.
    filename : str, opcional
        Nome base do arquivo (sem extensão). O padrão é "vra_master".
    timestamp : bool, opcional
        Se True, adiciona ao nome do arquivo um sufixo com data e hora
        no formato YYYYMMDD_HHMMSS, garantindo unicidade e versionamento.

    Notas
    -----
    - O diretório root/data/ é criado automaticamente caso não exista.
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
    df.to_csv(f'{filepath}.csv', index=False, encoding="utf-8")
    df.to_parquet(f'{filepath}.parquet', index=False)

    print(f"📁 Arquivos salvos com sucesso:")
    print(f"   → ./data/{filename_raw}.csv")
    print(f"   → ./data/{filename_raw}.parquet")

def main() -> None:
    '''
    Função principal para executar o processo ETL completo direto da linha de comando.
    '''
    urls = getUrls()
    master_dataframe = preprocess_csvs(urls)
    save_df(master_dataframe, timestamp=True)

    master_dataframe.info()
    master_dataframe.head()

if __name__ == "__main__":
    main()