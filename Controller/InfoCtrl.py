from Model.Info import Info
from DB.InfoDAO import InfoDAO

class InfoCtrl:
    # Traduzir comandos HTTP em ações negociais
    # Conceito REST
    # Considerar o protocolo HTTP

    async def gravar(self, requisicao):
        if requisicao.method == "POST" and requisicao.is_json:
            dados = requisicao.get_json()

            # pseudo validação
            if all(key in dados for key in ["nome", "descricao", "status", "urlImagem"]):
                servico = Info(
                    0,
                    dados["nome"],
                    dados["descricao"],
                    dados["status"],
                    dados["urlImagem"]
                )

                try:
                    servico.gravar()
                    return {
                        "status": True,
                        "mensagem": "Info gravada com sucesso!",
                        "id": servico.id
                    }, 201
                except Exception as error:
                    return {
                        "status": False,
                        "mensagem": f"Erro ao registrar a info: {error}"
                    }, 500
            else:
                return {
                    "status": False,
                    "mensagem": "Informe todos os dados necessários conforme documentação!"
                }, 400
        else:
            return {
                "status": False,
                "mensagem": "Formato não permitido!"
            }, 405

    async def alterar(self, requisicao):
        if requisicao.method in ["PUT", "PATCH"] and requisicao.is_json:
            dados = requisicao.get_json()

            # pseudo validação
            if all(key in dados for key in ["id", "nome", "descricao", "status", "urlImagem"]):
                servico = Info(
                    dados["id"],
                    dados["nome"],
                    dados["descricao"],
                    dados["status"],
                    dados["urlImagem"]
                )

                try:
                    servico.alterar()
                    return {
                        "status": True,
                        "mensagem": "Info alterada com sucesso!"
                    }, 200
                except Exception as error:
                    return {
                        "status": False,
                        "mensagem": f"Erro ao alterar a info: {error}"
                    }, 500
            else:
                return {
                    "status": False,
                    "mensagem": "Informe todos os dados necessários conforme documentação!"
                }, 400
        else:
            return {
                "status": False,
                "mensagem": "Formato não permitido!"
            }, 405

    async def excluir(self, requisicao):
        if requisicao.method == "DELETE" and requisicao.is_json:
            id = requisicao.view_args.get("id")  # O id deve ser informado na URL

            # pseudo validação
            if id and int(id) > 0:
                info = Info(int(id))

                try:
                    info.excluir()
                    return {
                        "status": True,
                        "mensagem": "Info excluída com sucesso!"
                    }, 200
                except Exception as error:
                    return {
                        "status": False,
                        "mensagem": f"Erro ao excluir a info: {error}"
                    }, 500
            else:
                return {
                    "status": False,
                    "mensagem": "Informe um id válido na URL!"
                }, 400
        else:
            return {
                "status": False,
                "mensagem": "Formato não permitido!"
            }, 405

    async def consultar(self, requisicao, info=None):
        termo_busca = info  # Recupera o termo da URL
        
        print(1)
        if requisicao.method == "GET":
            info_dao = InfoDAO()

            print(1.2)
            try:
                print(2.1)
                lista_infos = await info_dao.consultar(termo_busca)
                return {
                    "status": True,
                    "listaInfos": lista_infos
                }, 200
            except Exception as error:
                print(2.2)
                return {
                    "status": False,
                    "mensagem": f"Não foi possível recuperar as infos: {error}"
                }, 500
        else:
            print(1.3)
            return {
                "status": False,
                "mensagem": "Método não permitido!"
            }, 405
