from flask import Blueprint, request, render_template, jsonify
# import sys
import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from Controller.InfoCtrl import InfoCtrl

# Instanciar o controlador
info_ctrl = InfoCtrl()

# Criar o blueprint para as rotas
rota_info = Blueprint(
    'rota_info', 
    __name__, 
    template_folder=os.path.join(os.path.dirname(__file__), '../Public')
)

@rota_info.route('/home', methods=["GET"])
def home():
    print("Acessando a rota home", rota_info.template_folder)
    return render_template('index.html')

# Configurar as rotas
@rota_info.route("/", methods=["GET"])
async def consultar_tudo():
    resultado = await info_ctrl.consultar(request)  # Aguarda a execução da corrotina
    return jsonify(resultado)  # Garante que o retorno seja serializável em JSON

@rota_info.route("/<info>", methods=["GET"])
async def consultar_info(info):
    resultado = await info_ctrl.consultar(request, info=info)
    
    return jsonify(resultado)

@rota_info.route("/", methods=["POST"])
def gravar():
    resultado = info_ctrl.gravar(request)

    return jsonify(resultado)

@rota_info.route("/", methods=["PUT"])
def alterar():
    resultado = info_ctrl.alterar(request)

    return jsonify(resultado)

@rota_info.route("/<id>", methods=["DELETE"])
def excluir(id):
    resultado = info_ctrl.excluir(request, id=id)

    return jsonify(resultado)
