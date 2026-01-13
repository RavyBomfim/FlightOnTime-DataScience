# Model Documentation: LGBMClassifier

## Specifications
- **num_leaves**: `189`
- **boosting_type**: `gbdt`
- **learning_rate**: `0.1`
- **min_child_weight**: `0.001`
- **max_depth**: `-1`
- **reg_alpha**: `0.13860590871139572`
- **reg_lambda**: `1`
- **n_estimators**: `100`
- **class_weight**: `balanced`

## Expected Features
- Empresa Aérea
- Data Hora Voo
- Aeródromo Origem
- Aeródromo Destino
- Distância (m)

## Sample Input - X.head(1)

| Column Name       | First row value     | Dtype          |
| ----------------- | ------------------- | -------------- |
| Empresa Aérea     | AZU                 | category       |
| Aeródromo Origem  | SBKP                | category       |
| Aeródromo Destino | SBRP                | category       |
| Distância (m)     | 218000              | int32          |
| Data Hora Voo     | 2021-01-01 18:20:00 | datetime64[ns] |


## Sample Output - y.head()

| y_i | model.predict() | model.predict_proba() | dtype |
| --- | --------------- | --------------------- | ----- |
| y0  | 1               | [0.37,0.63]           | int8  |
| y1  | 0               | [0.87,0.13]           | int8  |
| y2  | 1               | [0.35,0.65]           | int8  |
| y3  | 0               | [0.59,0.41]           | int8  |
| y4  | 0               | [0.77,0.23]           | int8  |

