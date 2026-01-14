import pandas as pd
from helpers.plot_feature import plot_feature

def visualize_y(df: pd.DataFrame, y_col_name: str) -> None:
    """
    Exibe a distribuição da variável alvo e gera sua visualização gráfica.

    Parâmetros
    ----------
    df : pandas.DataFrame
        - DataFrame contendo a variável alvo.
    y_col_name : str
        - Nome da coluna correspondente à variável alvo.

    Retorna
    -------
    None
    """
    print(f'{df[y_col_name].value_counts()}\n')
    print(df[y_col_name].value_counts(normalize=True))
    plot_feature(df, y_col_name)