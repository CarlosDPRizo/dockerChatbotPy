from flask import Flask
from Routes.rotaInfo import rota_info
from Routes.rotaDF import rota_df
from dotenv import load_dotenv
from asgiref.wsgi import WsgiToAsgi
import os

# Configurações CRÍTICAS - devem vir antes de QUALQUER import do TF
os.environ['TF_DF_CUSTOM_OPS'] = 'false'  # Desativa operações C++
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Silencia logs do TF (0-3)
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'  # Desativa GPU

load_dotenv()

def create_app():
    MODEL_DIR = "modelos/tempo_saida_model"
    
    # Verificação segura do modelo
    model_ready = os.path.exists(MODEL_DIR) and os.listdir(MODEL_DIR)
    
    if not model_ready:
        print("🔵 Iniciando treinamento do modelo...")
        try:
            # Importação LOCAL para garantir configurações prévias
            from train import train_and_save_model
            train_and_save_model()
            print("✅ Modelo treinado com sucesso")
        except Exception as e:
            print(f"🔴 Falha crítica: {str(e)}")
            raise

    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False
    app.register_blueprint(rota_info, url_prefix="/info")
    app.register_blueprint(rota_df, url_prefix="/webhook")
    app.static_folder = './Public'
    return app

app = create_app()
asgi_app = WsgiToAsgi(app)

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 3000))
    print(f"🚀 Servidor iniciado em http://{host}:{port}")
    uvicorn.run(asgi_app, host=host, port=port, reload=False)