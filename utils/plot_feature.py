import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from utils.label_plot import label_plot
from utils.plot_central_tendency import plot_central_tendency

def plot_histplot(df: pd.DataFrame, feature: str) -> None:
    plt.figure(figsize=(6, 4))
    sns.histplot(list(df[feature]), kde=True, kde_kws={'bw_adjust': 0.5}, color='green', alpha=0.7)

    label_plot(title=f'Distribution of {feature}', xlabel=feature, ylabel='Frequency', fontsizes='large')
    plot_central_tendency(df[feature])
    
    plt.show()
    plt.close()

def plot_barplot(df: pd.DataFrame, feature: str) -> None:
    plt.figure(figsize=(6, 4))
    sns.barplot(x=df[feature].value_counts().index, y=df[feature].value_counts().values, palette='Set2', hue=df[feature].value_counts().index)

    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    minor_bar = min(df[feature].value_counts().values)
    greater_bar = max(df[feature].value_counts().values)
    plt.ylim(minor_bar * 0.35, greater_bar * 1.05)

    label_plot(title=f'Distribution of {feature}', xlabel=feature, ylabel='Frequency', fontsizes='large')
    for i, v in enumerate(df[feature].value_counts().values):
        plt.text(i, v, v, ha='center', va='bottom')

    if df[feature].unique().shape[0] > 3:
        plt.xticks(rotation=25)

    plt.tight_layout()
    plt.show()
    plt.close()

def plot_feature(df: pd.DataFrame, feature: str) -> None:
    if df[feature].dtype == 'int64' or df[feature].dtype == 'int32' or df[feature].dtype == 'int16' or df[feature].dtype == 'int8' or df[feature].dtype == 'float64' or df[feature].dtype == 'float32' or df[feature].dtype == 'float16' or df[feature].dtype == 'float8':
        plot_histplot(df, feature)
    else:
        plot_barplot(df, feature)