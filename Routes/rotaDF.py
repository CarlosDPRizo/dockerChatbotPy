from flask import Blueprint, request, jsonify
from Controller.DFCtrl import DFController

# Criação do blueprint para as rotas
rota_df = Blueprint('rota_df', __name__)
df_control = DFController()

# Definição da rota POST para processar intenções
@rota_df.route('/', methods=['POST'])
async def processar_intencoes():
    resultado = await df_control.processar_intencoes(request)

    return jsonify(resultado)
