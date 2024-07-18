from flask import Flask, request, jsonify
import numpy as np
from utils import model_dense_layer, preparar_dados, reverter_normalizacao, columns_to_scale

app = Flask(__name__)

@app.route('/predict_dense_layer/<variable>', methods=['POST'])
def predict(variable):
    data = request.get_json()
    input_data = preparar_dados(data)

    model_paths = {
        'temperatura': 'camada_densa/model_temperatura.weights.h5',
        'umidade': 'camada_densa/model_umidade.weights.h5',
        'chuva': 'camada_densa/model_chuva.weights.h5',
        'presao': 'camada_densa/model_presao.weights.h5',
        'radiacao': 'camada_densa/model_radiacao.weights.h5'
    }

    if variable not in model_paths:
        return jsonify({'error': 'Invalid variable'}), 400

    model = model_dense_layer(model_paths[variable])
    prediction = model.predict(input_data)
    prediction_value = prediction[0][0]

    # Obter o índice da variável na lista columns_to_scale
    column_index = columns_to_scale.index(variable)
    original_value = reverter_normalizacao(prediction_value, column_index)

    return jsonify({'prediction': float(original_value)})

if __name__ == '__main__':
    app.run(debug=True, port=8000)
