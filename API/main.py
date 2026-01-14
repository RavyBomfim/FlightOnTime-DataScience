import os
import datetime
import numpy as np
from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from API.predict import predict_delay

# Nome do modelo treinado a ser utilizado (sem extensão)
model_name = "flight_delay_LGBMClassifier_20260113_194452"

load_dotenv()
app = FastAPI()

# 🔐 Lê o token do ambiente (produção)
API_TOKEN = os.getenv("PREDICTION_API_TOKEN")
if not API_TOKEN:
    raise RuntimeError("PREDICTION_API_TOKEN não configurado!")

class PredictRequest(BaseModel):
    companhia: str
    origem: str
    destino: str
    data_partida: datetime.datetime
    distancia_m: int

class PredictResponse(BaseModel):
    previsao: int
    probabilidade: float

@app.post("/predict", response_model=PredictResponse)
def predict(data: PredictRequest, authorization: str = Header(None)):
    """
    Endpoint da API responsável por realizar a predição de atraso de voo.

    Parâmetros
    ----------
    data : PredictRequest
        - Dados de entrada validados para a predição.
    authorization : str, com valor padrão None
        - Token de autenticação enviado no header da requisição.

    Retorna
    -------
    PredictResponse
        - Objeto contendo a previsão de atraso e a probabilidade associada.

    Exceções
    --------
    HTTPException
        - Retornada com status 401 quando o token de autenticação é inexistente ou inválido.
    """
    if authorization != API_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Load your trained model and run inference
    result = predict_delay(model_name, dict(data))
    previsao = result["previsao"]
    probabilidade = round(np.float64(result["probabilidade"]), 2)

    return PredictResponse(
        previsao=previsao,
        probabilidade=probabilidade # type: ignore
    )