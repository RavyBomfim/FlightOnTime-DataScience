import os
import pickle
import automlx
import pandas as pd
from typing import Dict
from typing import Literal
from utils.evaluate_model import evaluate_model
from utils.export_model import export_model

def export_experimental_models(experimental_models: dict[str, automlx._interface]) -> None: # type: ignore
    # Garante que o diretório ./models/experimental_models exista
    experimental_models_dir = os.path.join(os.path.dirname(__file__), "..", "models", "experimental_models")
    experimental_models_dir = os.path.abspath(experimental_models_dir)
    os.makedirs(experimental_models_dir, exist_ok=True)

    # Exporta os modelos
    for name, estimator in experimental_models.items():
        export_model(
            estimator,
            filename=f'experimental_models/{name}',
            timestamp=False
        )

def run_experiments(
    pipeline_configs: Dict[str, dict],
    X_train: pd.DataFrame,
    y_train: pd.Series,
    time_budget: float = -1,
    cv: int|Literal["auto"] = "auto",
) -> dict[str, automlx._interface]: # type: ignore
    experimental_models = {}

    for name, config in pipeline_configs.items():
        print(f"\n{'='*60}")
        print(f"🚀 Running experiment: {name}")
        print(f"{'='*60}\n")

        pipeline = automlx.Pipeline(**config) # type: ignore

        estimator = pipeline.fit(
            X_train,
            y_train,
            time_budget=time_budget,
            cv=cv,
        )

        # Store for later inspection
        experimental_models[name] = estimator
    
    print(f"\n{'='*60}")
    print(f"🏁 All experiments completed!")
    print(f"{'='*60}\n")

    print("=> Exporting experimental models...\n")
    export_experimental_models(experimental_models)

    return experimental_models

def evaluate_experimental_models(
    experimental_models: dict[str, automlx._interface], # type: ignore
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> None:
    for name, estimator in experimental_models.items():
        print(f"\n{'='*60}")
        print(f"📊 Experiment results: {name}")
        print(f"{'='*60}\n")

        evaluate_model(estimator, X_test, y_test)

def load_experimental_models(pipeline_configs: dict[str, dict]) -> dict[str, automlx._interface]: # type: ignore
    print("Carregando modelos experimentais...\n")

    experimental_models_dir = os.path.join(
        os.path.dirname(__file__),
        "..",
        "models",
        "experimental_models"
    )
    experimental_models_dir = os.path.abspath(experimental_models_dir)

    loaded_models = {}

    for name in pipeline_configs.keys():
        model_path = os.path.join(experimental_models_dir, f"{name}.pkl")
        print(f"🔄 Carregando modelo: {name}")

        if not os.path.exists(model_path):
            print(f"⚠️  O modelo '{name}' não existe.\n")
            continue

        try:
            with open(model_path, "rb") as f:
                loaded_models[name] = pickle.load(f)

        except Exception as e:
            print(f"❌ Erro ao carregar o modelo '{name}': {e}\n")

    print("\n🏁 Modelos carregados com sucesso!")

    return loaded_models