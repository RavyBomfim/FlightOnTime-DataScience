import os
import pickle
import automlx
from datetime import datetime

def export_model(estimator: automlx._interface.classifier.AutoClassifier, filename: str, timestamp: bool = False) -> None: # type: ignore
    '''
    Exporta um modelo treinado para um arquivo pickle.

    Parâmetros
    ----------
    estimator : automlx._interface.classifier.AutoClassifier
        - Modelo treinado a ser salvo.
    filename : str
        - Nome do arquivo (sem extensão).
    timestamp : bool, opcional
        - Se True, adiciona ao nome do arquivo um sufixo com data e hora
        no formato YYYYMMDD_HHMMSS, garantindo unicidade e versionamento.

    Notas
    -----
    - O diretório ./models/ é criado automaticamente caso não exista.
    '''
    # Garante que o diretório ./models/ exista
    models_dir = os.path.join(os.path.dirname(__file__), "..", "models")
    models_dir = os.path.abspath(models_dir)
    os.makedirs(models_dir, exist_ok=True)

    # Se timestamp=True, adiciona YYYYMMDD_HHMMSS ao nome do arquivo
    filename_raw = filename
    if timestamp:
        base, ext = os.path.splitext(filename)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{base}_{ts}{ext}"
        filename_raw = f"{base}_{ts}"

    # Caminho completo para salvar o arquivo
    filepath = os.path.join(models_dir, filename)

    # Salva o modelo em um arquivo pickle
    with open(f'{filepath}.pkl', 'wb') as file:
        pickle.dump(estimator, file)

    print(f"📁 Arquivo salvo com sucesso:")
    print(f"   → ./models/{filename_raw}.pkl")