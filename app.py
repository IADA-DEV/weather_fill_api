from flask import Flask, request, jsonify
import numpy as np
from utils import model_dense_layer, preparar_dados, reverter_normalizacao, columns_to_scale

app = Flask(__name__)

@app.route('/predict_dense_layer', methods=['POST'])
def predict():
    data = request.get_json()
    input_data = preparar_dados(data)

    model_paths = {
        'temperatura': 'camada_densa/model_temperatura.weights.h5',
        'umidade': 'camada_densa/model_umidade.weights.h5',
        'chuva': 'camada_densa/model_chuva.weights.h5',
        'presao': 'camada_densa/model_presao.weights.h5',
        'radiacao': 'camada_densa/model_radiacao.weights.h5'
    }

    predictions = {}

    for variable, model_path in model_paths.items():
        model = model_dense_layer(model_path)
        prediction = model.predict(input_data)
        prediction_value = prediction[0][0]

        # Obter o índice da variável na lista columns_to_scale
        column_index = columns_to_scale.index(variable)
        original_value = reverter_normalizacao(prediction_value, column_index)

        predictions[variable] = float(original_value)

    response = {
        "rl": predictions,  
        "cd": predictions
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
