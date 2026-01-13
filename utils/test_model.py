import os
import pickle
import pandas as pd

def test_model(model_filename: str, X_test: pd.DataFrame):
    models_dir = os.path.join(os.path.dirname(__file__), "..", "models")
    models_dir = os.path.abspath(models_dir)

    model_path = os.path.join(models_dir, model_filename.replace('.pkl', ''))
    model = pickle.load(open(f'{model_path}.pkl', 'rb'))

    print(f"\n{'='*60}")
    print(f"📊 Testing model: {model_filename}")
    print(f"{'='*60}\n")

    print("Test data columns:")
    print(X_test.columns)

    pred = model.predict(X_test.head(10))
    proba = model.predict_proba(X_test.head(10))
    predictions = pd.DataFrame({
        'Prediction': pred,
        'Probability_Class_0': proba[:, 0],
        'Probability_Class_1': proba[:, 1]
    })

    print("\nPredictions on first 10 samples:\n")
    print(predictions.head(10))