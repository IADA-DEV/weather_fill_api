from sklearn.preprocessing import StandardScaler
from datetime import datetime
import numpy as np
import pandas as pd
import tensorflow as tf
import joblib

# Carregar o scaler salvo
scaler = joblib.load('scaler.pkl')

# Selecionar as colunas específicas para normalização
columns_to_scale = ['temperatura', 'umidade', 'chuva', 'presao', 'radiacao']

# Função para carregar o modelo com pesos específicos
def model_dense_layer(weights_path):
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(units=32, activation='relu', input_shape=(13,)),
        tf.keras.layers.Dense(units=1)
    ])
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    model.load_weights(weights_path)
    return model

# Funções auxiliares
def calcular_wx_wy(data):
    vento = data.pop('vento')
    vd_vento = data.pop('vento_dir')
    vd_vento_rad = vd_vento * np.pi / 180

    data['Wx'] = vento * np.cos(vd_vento_rad)
    data['Wy'] = vento * np.sin(vd_vento_rad)
    return data

def calcular_tempos(data):
    date_time_str = data.pop('d_time')
    date_time = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
    timestamp_s = date_time.timestamp()

    day = 24 * 60 * 60
    year = (365.2425) * day

    data['Day sin'] = np.sin(timestamp_s * (2 * np.pi / day))
    data['Day cos'] = np.cos(timestamp_s * (2 * np.pi / day))
    data['Year sin'] = np.sin(timestamp_s * (2 * np.pi / year))
    data['Year cos'] = np.cos(timestamp_s * (2 * np.pi / year))

    return data

def normalizar_dados(data):
    data_to_scale = {k: data[k] for k in columns_to_scale}
    data_to_keep = {k: data[k] for k in data if k not in columns_to_scale}

    df_to_scale = pd.DataFrame([data_to_scale])
    scaled_values = scaler.transform(df_to_scale)

    data_normalized = {columns_to_scale[i]: scaled_values[0][i] for i in range(len(columns_to_scale))}
    data_normalized.update(data_to_keep)
    
    return data_normalized

def reverter_normalizacao(prediction, column_index):
    dummy_data = np.zeros((1, scaler.scale_.shape[0]))
    dummy_data[0, column_index] = prediction
    inversed = scaler.inverse_transform(dummy_data)
    return inversed[0, column_index]

def preparar_dados(data):
    data = calcular_wx_wy(data)
    data = calcular_tempos(data)
    data = normalizar_dados(data)
    colunas_x = ['temperatura', 'chuva', 'umidade', 'radiacao', 'presao',
                 'Day sin', 'Day cos', 'Year sin', 'Year cos',
                 'Wx', 'Wy', 'distancia', 'dif_altura']
    input_data = np.array([[data[col] for col in colunas_x]])
    return input_data
