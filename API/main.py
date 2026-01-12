import os
import datetime
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from API.predict import predict_delay
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# 🔐 Lê o token do ambiente (produção)
API_TOKEN = os.getenv("PREDICTION_API_TOKEN")

if not API_TOKEN:
    raise RuntimeError("PREDICTION_API_TOKEN não configurado!")

# Nome do modelo treinado a ser utilizado (sem extensão)
model_name = "flight_delay_XGBClassifier_20260108_173529"

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
def predict(data: PredictRequest, Authorization: str = Header(None)):

    if Authorization != API_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Load your trained model and run inference
    result = predict_delay(model_name, dict(data))
    previsao = result["previsao"]
    probabilidade = result["probabilidade"]

    return PredictResponse(
        previsao=previsao,
        probabilidade=probabilidade
    )