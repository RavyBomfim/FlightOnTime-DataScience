import time
import datetime
import automlx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def plot_algorithm_selection(estimator: automlx._interface.classifier.AutoClassifier) -> None: # type: ignore
    '''
        Exibe um gráfico de barras comparando o desempenho dos algoritmos testados
        na etapa de seleção de modelo.  

        - Cada experimento (`trial`) é uma linha em um dataframe que contém:  
        Algoritmo, Número de Amostras, Número de Features, Hiperparâmetros, Score, Tempo de Execução, Uso de Memória e Etapa

        Parâmetros
        ----------
        estimator : automlx._interface.classifier.AutoClassifier
            - Estimador treinado pelo Oracle AutoMLx, contendo o resumo dos experimentos e o modelo selecionado.

        Retorno
        -------
        None
    '''
    trials = estimator.completed_trials_summary_[estimator.completed_trials_summary_["Step"].str.contains('Model Selection')]
    name_of_score_column = f"Score ({estimator._inferred_score_metric[0].name})"

    trials.replace([np.inf, -np.inf], np.nan, inplace=True)
    trials.dropna(subset=[name_of_score_column], inplace = True)
    scores = trials[name_of_score_column].tolist()
    models = trials['Algorithm'].tolist()
    colors = []

    y_margin = 0.10 * (max(scores) - min(scores))
    s = pd.Series(scores, index=models).sort_values(ascending=False)
    s = s.dropna()
    for f in s.keys():
        if f.strip()  ==  estimator.selected_model_.strip():
            colors.append('orange')
        elif s[f] >= s.mean():
            colors.append('teal')
        else:
            colors.append('turquoise')

    fig, ax = plt.subplots(1)
    ax.set_title("Algorithm Selection Trials")
    ax.set_ylim(min(scores) - y_margin, max(scores) + y_margin)
    ax.set_ylabel(estimator._inferred_score_metric[0].name)
    s.plot.bar(ax=ax, color=colors, edgecolor='black')
    ax.axhline(y=s.mean(), color='black', linewidth=0.5)
    plt.show()
    plt.close()

def plot_adaptive_sampling(estimator: automlx._interface.classifier.AutoClassifier) -> None: # type: ignore
    '''
        Exibe um gráfico de linha relacionando o tamanho da amostra do dataset
        com o score obtido em cada experimento.  

        - Cada experimento (`trial`) é uma linha em um dataframe que contém:  
        Algoritmo, Número de Amostras, Número de Features, Hiperparâmetros, Score, Tempo de Execução, Uso de Memória e Etapa

        Parâmetros
        ----------
        estimator : automlx._interface.classifier.AutoClassifier
            - Estimador treinado pelo Oracle AutoMLx, contendo os resultados da etapa de amostragem adaptativa.

        Retorno
        -------
        None
    '''
    trials = estimator.completed_trials_summary_[estimator.completed_trials_summary_["Step"].str.contains('Adaptive Sampling')]
    name_of_score_column = f"Score ({estimator._inferred_score_metric[0].name})"

    trials.replace([np.inf, -np.inf], np.nan, inplace=True)
    trials.dropna(subset=[name_of_score_column], inplace = True)
    scores = trials[name_of_score_column].tolist()
    n_samples = [int(sum(d.values()) / len(d)) if isinstance(d, dict) else d for d in trials['# Samples']]


    y_margin = 0.10 * (max(scores) - min(scores))
    fig, ax = plt.subplots(1)
    ax.set_title("Adaptive Sampling ({})".format(estimator.selected_model_))
    ax.set_xlabel('Dataset sample size')
    ax.set_ylabel(estimator._inferred_score_metric[0].name)
    ax.grid(color='g', linestyle='-', linewidth=0.1)
    ax.set_ylim(min(scores) - y_margin, max(scores) + y_margin)
    ax.plot(n_samples, scores, 'k:', marker="s", color='teal', markersize=3)
    plt.show()
    plt.close()

def plot_feature_selection(estimator: automlx._interface.classifier.AutoClassifier, df: pd.DataFrame) -> None: # type: ignore
    '''
        Exibe no console as features selecionadas e descartadas e apresenta
        um gráfico do score em função do número de features testadas.  

        - Cada experimento (`trial`) é uma linha em um dataframe que contém:  
        Algoritmo, Número de Amostras, Número de Features, Hiperparâmetros, Score, Tempo de Execução, Uso de Memória e Etapa

        Parâmetros
        ----------
        estimator : automlx._interface.classifier.AutoClassifier
            - Estimador treinado pelo Oracle AutoMLx, contendo informações sobre as features selecionadas.
        df : pandas.DataFrame
            - DataFrame original utilizado no treinamento, contendo todas as features.

        Retorno
        -------
        None
    '''
    # Exibe as features selecionadas e as descartadas
    print(f"Features selected: {estimator.selected_features_names_}")
    dropped_features = df.drop(estimator.selected_features_names_raw_, axis=1).columns
    print(f"Features dropped: {dropped_features.to_list()}")

    trials = estimator.completed_trials_summary_[estimator.completed_trials_summary_["Step"].str.contains('Feature Selection')]
    name_of_score_column = f"Score ({estimator._inferred_score_metric[0].name})"

    trials.replace([np.inf, -np.inf], np.nan, inplace=True)
    trials.dropna(subset=[name_of_score_column], inplace = True)
    trials.sort_values(by=['# Features'],ascending=True, inplace = True)
    scores = trials[name_of_score_column].tolist()
    n_features = trials['# Features'].tolist()

    y_margin = 0.10 * (max(scores) - min(scores))
    fig, ax = plt.subplots(1)
    ax.set_title("Feature Selection Trials")
    ax.set_xlabel("Number of Features")
    ax.set_ylabel(estimator._inferred_score_metric[0].name)
    ax.grid(color='g', linestyle='-', linewidth=0.1)
    ax.set_ylim(min(scores) - y_margin, max(scores) + y_margin)
    ax.plot(n_features, scores, 'k:', marker="s", color='teal', markersize=3)
    ax.axvline(x=len(estimator.selected_features_names_), color='orange', linewidth=2.0)
    plt.show()
    plt.close()

def plot_model_tuning(estimator: automlx._interface.classifier.AutoClassifier) -> None: # type: ignore
    '''
        Exibe um gráfico mostrando a evolução do melhor score ao longo das
        iterações de tuning de hiperparâmetros.  
        
        - Cada experimento (`trial`) é uma linha em um dataframe que contém:  
        Algoritmo, Número de Amostras, Número de Features, Hiperparâmetros, Score, Tempo de Execução, Uso de Memória e Etapa

        Parâmetros
        ----------
        estimator : automlx._interface.classifier.AutoClassifier
            - Estimador treinado pelo Oracle AutoMLx, contendo os resultados da etapa de ajuste de hiperparâmetros.

        Retorno
        -------
        None
    '''
    trials = estimator.completed_trials_summary_[estimator.completed_trials_summary_["Step"].str.contains('Model Tuning')]
    name_of_score_column = f"Score ({estimator._inferred_score_metric[0].name})"

    trials.replace([np.inf, -np.inf], np.nan, inplace=True)
    trials.dropna(subset=[name_of_score_column], inplace = True)
    trials.drop(trials[trials['Finished'] == -1].index, inplace = True)
    trials['Finished']= trials['Finished'].apply(lambda x: time.mktime(datetime.datetime.strptime(x,
                                                "%a %b %d %H:%M:%S %Y").timetuple()))
    trials.sort_values(by=['Finished'],ascending=True, inplace = True)
    scores = trials[name_of_score_column].tolist()
    score = []
    score.append(scores[0])
    for i in range(1,len(scores)):
        if scores[i]>= score[i-1]:
            score.append(scores[i])
        else:
            score.append(score[i-1])
    y_margin = 0.10 * (max(score) - min(score))

    fig, ax = plt.subplots(1)
    ax.set_title("Hyperparameter Tuning Trials")
    ax.set_xlabel("Iteration $n$")
    ax.set_ylabel(estimator._inferred_score_metric[0].name)
    ax.grid(color='g', linestyle='-', linewidth=0.1)
    ax.set_ylim(min(score) - y_margin, max(score) + y_margin)
    ax.plot(range(1, len(trials) + 1), score, 'k:', marker="s", color='teal', markersize=3)
    plt.show()
    plt.close()