import pickle
import pandas as pd

def test_model(model_filename: str, X_test: pd.DataFrame):
    model_path = f'./models/{model_filename}'
    model = pickle.load(open(model_path, 'rb'))
    print(X_test.columns)
    model.predict(X_test.head())