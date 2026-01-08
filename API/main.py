import datetime
from fastapi import FastAPI
from pydantic import BaseModel
from API.predict import predict_delay

app = FastAPI()
model_name = "flight_delay_XGBClassifier_20260108_173529.pkl"

class PredictRequest(BaseModel):
    companhia: str
    origem: str
    destino: str
    data_partida: datetime.datetime
    distancia_m: int

class PredictResponse(BaseModel):
    previsao: str
    probabilidade: float

@app.post("/predict", response_model=PredictResponse)
def predict(data: PredictRequest):
    # Load your trained model and run inference
    result = predict_delay(model_name, dict(data))
    previsao = result["previsao"]
    probabilidade = result["probabilidade"]

    return PredictResponse(
        previsao=previsao,
        probabilidade=probabilidade
    )