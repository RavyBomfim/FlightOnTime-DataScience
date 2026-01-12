import os
import pickle
import automlx
import pandas as pd
from helpers.parsers import parse_categoricals, parse_datetime, parse_int

def validate_features(
    feature_mapping: dict,
    estimator: automlx._interface.classifier.AutoClassifier  # type: ignore
) -> None:
    expected = set(estimator.selected_features_names_raw_)
    provided = set(feature_mapping.values())

    if expected != provided:
        raise ValueError(
            "Feature mismatch between model and inference mapping.\n"
            f"Model expects: {expected}\n"
            f"Mapping provides: {provided}"
        )

def transform_input(
    input_data: dict,
    estimator: automlx._interface.classifier.AutoClassifier  # type: ignore
) -> pd.DataFrame:
    FEATURE_MAPPING = {
        "companhia": "Empresa Aérea",
        "origem": "Aeródromo Origem",
        "destino": "Aeródromo Destino",
        "distancia_m": "Distância (m)",
        "data_partida": "Data Hora Voo",
    }

    validate_features(feature_mapping=FEATURE_MAPPING, estimator=estimator)

    df = pd.DataFrame()
    idx = 0

    for input_key, model_feature in FEATURE_MAPPING.items():
        if input_key not in input_data:
            raise ValueError(f"Missing required field: {input_key}")

        value = input_data[input_key]
        df.loc[idx, model_feature] = value

    df = parse_categoricals(df)
    df = parse_datetime(df)
    df = parse_int(df, col="Distância (m)", int_type="int32")

    return df

def predict_delay(model_filename: str, input_data: dict) -> dict:
    models_dir = os.path.join(os.path.dirname(__file__), "..", "models")
    models_dir = os.path.abspath(models_dir)
    model_path = f'{models_dir}/{model_filename}.pkl'

    model = pickle.load(open(model_path, 'rb'))
    x = transform_input(input_data, model)

    pred = model.predict(x)
    proba = model.predict_proba(x)

    predictions = {
        "previsao": pred,
        "probabilidade": proba[0][1]
    }

    return predictions