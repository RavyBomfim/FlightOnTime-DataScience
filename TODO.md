# To do list

## -> API

1. Remover chave "distancia_km" e adicionar "código tipo linha" (nomenclatura a definir)

## -> Modelo

1. Remover NaN da variável "Código Tipo Linha" 

2. Comparar "Partida Prevista" e "Partida Real" para derivar se atrasou
    - Criar coluna "Atrasou": Type=int  
    
    - Se "Partida Real" > "Partida Prevista"
    - "Atrasou" == 1
    - Else: "Atrasou" == 0

3. Dropar "Partida Prevista" e "Partida Real"

4. Separar treino e teste (70/30)

5. Verificar balanceamento:
    - Se necessário fazer resampling (smote ?)

6. Fazer validação cruzada (k-fold / stratified k-fold)

7. Testar modelos (random forest, decision tree, logistic regression, KNN etc.) e hiperparâmetros (Oracle AutoML / Biblioteca Advanced Data Science - ADS)

8. Avaliação...

8. Resolver se deve mensurar ``recall`` ou ``precisão``

É melhor achar (modelo prevê) que vai atrasar (1) e não atrasar (fato) (0)