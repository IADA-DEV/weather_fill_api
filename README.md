# WeatherFillAPI

WeatherFillAPI é uma API projetada para completar dados ausentes em bancos de dados meteorológicos. Utilizando métodos de regressão linear e redes neurais de camada densa, a API preenche lacunas em conjuntos de dados climáticos, melhorando a precisão e a consistência das análises meteorológicas. A API trabalha exclusivamente com dados fornecidos pelo INMET (Instituto Nacional de Meteorologia).

## Funcionalidades

- **Preenchimento de Dados Ausentes:** Utiliza algoritmos de regressão linear e redes neurais de camada densa para prever e preencher valores ausentes.
- **Integração com Estações Vizinhas:** Recebe dados de estações meteorológicas vizinhas para melhorar a precisão das previsões.
- **Vários Parâmetros Climáticos:** Processa múltiplos parâmetros como temperatura, chuva, umidade, radiação, pressão e vento.

## Estrutura do Projeto

O arquivo principal do projeto é o `app.py`, que contém a definição da API usando Flask.

## Exemplo de Requisição

A API espera uma requisição HTTP POST na rota específica para o parâmetro que se deseja completar. 

**Rota:**

POST http://127.0.0.1:8000/predict_dense_layer/radiacao


**Formato do Corpo da Requisição:**

```json
{
    "temperatura": 22.6,
    "chuva": 0,
    "umidade": 61.0,
    "radiacao": 1506.0,
    "presao": 888.2,
    "vento": 1.8,
    "vento_dir": 126.0,
    "d_time": "2000-05-07 12:00:00",
    "distancia": 10,
    "dif_altura": 5
}
```

** Resposta
```json
{
    "radiacao": 1450.0
}
```



# Notas
- ** Esta API foi projetada para completar dados meteorológicos especificamente do INMET.
- ** Certifique-se de que os dados enviados estejam no formato esperado para obter previsões precisas.
