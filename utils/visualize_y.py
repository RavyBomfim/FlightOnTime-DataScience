import pandas as pd
from helpers.plot_feature import plot_feature

def visualize_y(df: pd.DataFrame, y_col_name: str) -> None:
    print(f'{df[y_col_name].value_counts()}\n')
    print(df[y_col_name].value_counts(normalize=True))
    plot_feature(df, y_col_name)