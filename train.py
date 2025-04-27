import os
import sys
from datetime import datetime
import pandas as pd

# CONFIGURAÇÕES ESSENCIAIS (primeiras linhas do arquivo)
os.environ['TF_DF_CUSTOM_OPS'] = 'false'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

MODEL_DIR = "modelos/tempo_saida_model"

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%d/%m/%Y")
    except ValueError:
        return None

def train_and_save_model():
    print("=== INÍCIO DO TREINAMENTO ===")
    
    if not os.path.isfile('ocorrencias_com_agendamento.csv'):
        print("❌ Arquivo CSV 'ocorrencias_com_agendamento.csv' não encontrado no diretório:", os.getcwd())
        sys.exit(1)
    
    try:
        import tensorflow_decision_forests as tfdf  # <- Importação dentro da função

        # 1. Carregamento de dados
        if not os.path.exists("occorrencias_com_agendamento.csv"):
            raise FileNotFoundError("Arquivo CSV não encontrado")
            
        df = pd.read_csv("occorrencias_com_agendamento.csv")
        
        # 2. Processamento
        df['data'] = df['data'].apply(parse_date)
        df['data_agendamento'] = df['data_agendamento'].apply(parse_date)
        
        if df['diferenca_dias'].isnull().any():
            raise ValueError("Valores nulos na coluna alvo")
            
        # 3. Modelo com configuração segura
        model = tfdf.keras.RandomForestModel(
            task=tfdf.keras.Task.REGRESSION,
            num_trees=100,
            max_depth=16,
            check_dataset=False
        )
        
        # 4. Treinamento
        dataset = tfdf.keras.pd_dataframe_to_tf_dataset(df, label="diferenca_dias")
        model.fit(dataset)
        
        # 5. Salvamento
        os.makedirs(MODEL_DIR, exist_ok=True)
        model.save(MODEL_DIR, save_format="tf")
        
        print(f"✅ Modelo salvo em {MODEL_DIR}")
        return True
        
    except Exception as e:
        print(f"❌ Erro no treinamento: {str(e)}")
        return False

if __name__ == "__main__":
    train_and_save_model()
