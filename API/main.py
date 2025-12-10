from fastapi import FastAPI
from pydantic import BaseModel
import datetime

app = FastAPI()

class PredictRequest(BaseModel):
    companhia: str
    origem: str
    destino: str
    data_partida: datetime.datetime
    distancia_km: int

class PredictResponse(BaseModel):
    previsao: str
    probabilidade: float

@app.post("/predict", response_model=PredictResponse)
def predict(data: PredictRequest):
    # Load your trained model and run inference
    # result = model.predict(...)
    
    # Dummy logic example:
    if data.distancia_km < 400:
        previsao = "Pontual"
        probabilidade = 0.22
    else:
        previsao = "Atraso"
        probabilidade = 0.57

    return PredictResponse(
        previsao=previsao,
        probabilidade=probabilidade
    )