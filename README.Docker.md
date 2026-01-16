# 🐳 Docker - FlightOnTime API

Este guia mostra como executar a API de predição de atrasos de voos usando Docker.

## 📋 Pré-requisitos

- Docker instalado ([Download Docker](https://www.docker.com/products/docker-desktop))
- Docker Compose instalado (geralmente vem com o Docker Desktop)

## 🚀 Executando com Docker

### Opção 1: Docker Compose (Recomendado)

1. **Configure a variável de ambiente**

   Crie um arquivo `.env` na raiz do projeto:

   ```bash
   PREDICTION_API_TOKEN=seu_token_secreto_aqui
   ```

2. **Execute o projeto**

   ```bash
   docker-compose up -d
   ```

3. **Verifique os logs**

   ```bash
   docker-compose logs -f
   ```

4. **Acesse a API**

   - Documentação interativa: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

5. **Parar o serviço**
   ```bash
   docker-compose down
   ```

### Opção 2: Docker direto

1. **Build da imagem**

   ```bash
   docker build -t flightontime-api .
   ```

2. **Execute o container**

   ```bash
   docker run -d \
     --name flightontime-api \
     -p 8000:8000 \
     -e PREDICTION_API_TOKEN=seu_token_secreto \
     -v $(pwd)/models:/app/models \
     -v $(pwd)/data:/app/data \
     -v $(pwd)/metadata:/app/metadata \
     flightontime-api
   ```

3. **Verificar logs**

   ```bash
   docker logs -f flightontime-api
   ```

4. **Parar o container**
   ```bash
   docker stop flightontime-api
   docker rm flightontime-api
   ```

## 🧪 Testando a API

Com o container rodando, teste o endpoint de predição:

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Authorization: seu_token_secreto" \
  -H "Content-Type: application/json" \
  -d '{
    "companhia": "AZUL",
    "origem": "SBGR",
    "destino": "SBPA",
    "data_partida": "2026-01-15T14:30:00",
    "distancia_m": 850000
  }'
```

## 📁 Volumes

O container monta os seguintes volumes para persistência:

- `./models` - Modelos treinados
- `./data` - Dados de treino/teste
- `./metadata` - Metadados (aeroportos, etc.)

## 🔧 Comandos Úteis

### Reconstruir a imagem

```bash
docker-compose build --no-cache
```

### Ver containers em execução

```bash
docker ps
```

### Executar comandos dentro do container

```bash
docker exec -it flightontime-api bash
```

### Verificar uso de recursos

```bash
docker stats flightontime-api
```

## ⚙️ Variáveis de Ambiente

| Variável               | Descrição                      | Obrigatória |
| ---------------------- | ------------------------------ | ----------- |
| `PREDICTION_API_TOKEN` | Token para autenticação da API | Sim         |

## 🐛 Troubleshooting

### A API não está respondendo

```bash
# Verifique os logs
docker-compose logs flightontime-api

# Verifique se o container está rodando
docker ps -a
```

### Erro de porta já em uso

```bash
# Mude a porta no docker-compose.yml
ports:
  - "8001:8000"  # Use 8001 ao invés de 8000
```

### Modelo não encontrado

```bash
# Certifique-se que os modelos estão no diretório ./models
ls -la models/

# Verifique os volumes montados
docker inspect flightontime-api
```

## 📝 Notas

- A imagem é otimizada para produção (slim base image)
- O `.dockerignore` exclui arquivos desnecessários
- Os volumes permitem atualizar modelos sem reconstruir a imagem
- O healthcheck monitora a saúde da aplicação
