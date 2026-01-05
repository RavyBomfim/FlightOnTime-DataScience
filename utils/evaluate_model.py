import automlx
import numpy as np
import pandas as pd

from sklearn.metrics import classification_report
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.metrics import roc_auc_score, confusion_matrix

def evaluate_model(estimator: automlx._interface.classifier.AutoClassifier, X_test: pd.DataFrame, y_test: pd.Series) -> None: # type: ignore
    '''
        Calcula e exibe métricas de avaliação do modelo no conjunto de teste,
        incluindo ROC AUC, relatório de classificação e matriz de confusão
        normalizada.
        
        Parâmetros
        ----------
        estimator : automlx._interface.classifier.AutoClassifier
            - Estimador treinado pelo Oracle AutoMLx, utilizado para gerar predições e probabilidades sobre o conjunto de teste.
        X_test : pandas.DataFrame
            - Conjunto de dados de teste, contendo as features utilizadas no treinamento.
        y_test : pandas.Series
            - Conjunto de dados de teste, contendo as classes a serem preditas.

        Retorno
        -------
        None
    '''
    y_pred = estimator.predict(X_test)
    y_proba = estimator.predict_proba(X_test)

    cm = confusion_matrix(y_test.astype(int), y_pred, labels=[False, True])
    cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    disp = ConfusionMatrixDisplay(
        confusion_matrix=cm,
        display_labels=["Não Atrasou", "Atrasou"]
    )

    score_default = roc_auc_score(y_test, y_proba[:, 1])

    print(f'=> Roc_auc score em dados de teste: {score_default}\n')
    print('=> Relatório de Classificação:\n')
    print(classification_report(y_test, y_pred))
    print('=> Matriz de Confusão:')
    disp.plot(cmap="viridis")