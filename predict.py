import tensorflow as tf
from datetime import datetime, timedelta
import os

MODEL_DIR = "modelos/tempo_saida_model"

print(f"Conteúdo do diretório: {os.listdir(MODEL_DIR)}")
# Carrega o modelo diretamente com tf.keras (forma recomendada)
model = tf.keras.models.load_model(MODEL_DIR)

def predict(input_data):
    try:
        # Converte a data de entrada
        data_entrada = datetime.strptime(input_data["data"], "%d/%m/%Y")
        
        # Prepara os dados de entrada no formato esperado pelo modelo
        # (Ajuste conforme a estrutura exata que seu modelo espera)
        input_features = {
            'feature1': tf.convert_to_tensor([input_data["valor1"]]),
            'feature2': tf.convert_to_tensor([input_data["valor2"]])
        }
        
        # Faz a previsão
        prediction = model(input_features)  # Chamada direta para modelos TF2.x+
        
        # Processa a saída
        diferenca_dias = float(prediction[0][0])
        data_agendamento_prevista = data_entrada + timedelta(days=diferenca_dias)
        
        return data_agendamento_prevista.strftime("%d/%m/%Y")
    
    except Exception as e:
        print(f"Erro na previsão: {str(e)}")
        return None