from Model.LogInfo import LogInfo
from DialogFlow.funcoes import obter_cards_infos
from DB.InfoDAO import InfoDAO

global_dados = {}  # Variável global para armazenar sessões
# Estudar a utilização do Redis para armazenar os dados das sessões

class DFController:
    async def processar_intencoes(self, req):
        if req.method == "POST" and req.is_json:
            dados = req.get_json()
            intencao = dados["queryResult"]["intent"]["displayName"]
            origem = dados.get("originalDetectIntentRequest", {}).get("source", "")
            resposta = {}

            if intencao == "InformarProtocoloNome":
                resposta = await self.exibir_menu(origem)
            elif intencao == "ApresentarOpcoes":
                resposta = await self.processar_escolha(dados, origem)
            elif intencao == "ConcluirInformarProtocoloNome":
                resposta = await self.devolver_escolhas(dados, origem)
            elif intencao == "AvaliarConversa":
                resposta = await self.registrar_log(dados, origem)

            return resposta

    async def exibir_menu(self, tipo=""):
        resposta = {"fulfillmentMessages": []}
        try:
            cards = await obter_cards_infos(tipo)

            if tipo == "custom":
                resposta["fulfillmentMessages"].append({
                    "text": {
                        "text": [
                            "Tudo certo, Carlos! \n",
                            "Estamos disponíveis 24h por dia e 7 na semana. \n",
                            "Estamos preparados para te ajudar com as seguintes informações: \n"
                        ]
                    }
                })
                resposta["fulfillmentMessages"].extend(cards)
                resposta["fulfillmentMessages"].append({
                    "text": {
                        "text": ["Por favor nos informe o que você deseja."]
                    }
                })
            else:
                resposta["fulfillmentMessages"].append({
                    "payload": {
                        "richContent": [[{
                            "type": "description",
                            "title": "Tudo certo, Carlos!",
                            "text": [
                                "Estamos disponíveis 24h por dia e 7 na semana. \n",
                                "Estamos preparados para te ajudar com as seguintes informações: \n"
                            ]
                        }]]
                    }
                })
                resposta["fulfillmentMessages"][0]["payload"]["richContent"][0].extend(cards)
                resposta["fulfillmentMessages"][0]["payload"]["richContent"][0].append({
                    "type": "description",
                    "title": "Por favor nos informe o que você deseja.",
                    "text": []
                })

        except Exception:
            mensagem_erro = [
                "Não foi possível recuperar a lista de informações disponíveis.",
                "Desculpe-nos pelo transtorno!",
                "Entre em contato conosco por telefone ☎ (18) 3226-1515."
            ]
            if tipo == "custom":
                resposta["fulfillmentMessages"].append({
                    "text": {"text": mensagem_erro}
                })
            else:
                resposta["fulfillmentMessages"].append({
                    "payload": {
                        "richContent": [[{
                            "type": "description",
                            "title": mensagem_erro[0],
                            "text": mensagem_erro[1:]
                        }]]
                    }
                })

        return resposta

    async def processar_escolha(self, dados, origem):
        sessao = dados["session"].split("/")[-1]
        if sessao not in global_dados:
            global_dados[sessao] = {"infos": []}

        infos_selecionadas = dados["queryResult"]["parameters"]["informacoes"]

        if isinstance(infos_selecionadas, str):
            infos_selecionadas = [infos_selecionadas]
    
        global_dados[sessao]["infos"].extend(infos_selecionadas)

        lista_mensagens = []
        for inf in infos_selecionadas:
            info_dao = InfoDAO()
            resultado = await info_dao.consultar(inf)

            if resultado:
                lista_mensagens.append(f"✅ {inf} registrado com sucesso! \n")
            else:
                lista_mensagens.append(f"❌ O {inf} não está disponível! \n")

        lista_mensagens.append("Posso te ajudar em algo mais?")
        resposta = {"fulfillmentMessages": []}

        if origem:
            resposta["fulfillmentMessages"].append({
                "text": {"text": lista_mensagens}
            })
        else:
            resposta["fulfillmentMessages"].append({
                "payload": {
                    "richContent": [[{
                        "type": "description",
                        "title": "",
                        "text": lista_mensagens
                    }]]
                }
            })

        return resposta

    async def devolver_escolhas(self, dados, origem):
        sessao = dados["session"].split("/")[-1]
        info_selecionadas = global_dados[sessao]["infos"]

        lista_mensagens = ["Essas são as informações que solicitou: \n"]
        info_dao = InfoDAO()
        for inf in info_selecionadas:
            busca = await info_dao.consultar(inf)
            if busca:
                status = busca[0].get("status")

            # Se status for vazio ou None, faz a previsão com o modelo 
            # Utilização de valores estáticos para mostrar a viabilidade
            if not status:
                input_data = {
                    "protocol": "2025-04-26",
                    "data": "26/04/2025",
                    "veiculo": "VW - VOLKSWAGEM - FOX 1.6 - 2005"
                }

                try:
                    from predict import predict
                    data_prevista = predict(input_data)
                    status = f"⏱️ Previsão de agendamento: {data_prevista}"
                except Exception as e:
                    status = f"⚠️ Erro na previsão: {str(e)}"

            lista_mensagens.append(f"➡️ {busca[0]['descricao']}: {status} \n")

        lista_mensagens.append("Obrigado pela paciência, por favor avalie o atendimento com uma nota de 0 a 10.")

        resposta = {"fulfillmentMessages": []}
        if origem:
            resposta["fulfillmentMessages"].append({
                "text": {"text": lista_mensagens}
            })
        else:
            resposta["fulfillmentMessages"].append({
                "payload": {
                    "richContent": [[{
                        "type": "description",
                        "title": "",
                        "text": lista_mensagens
                    }]]
                }
            })

        return resposta

    async def registrar_log(self, dados, origem):
        sessao = dados["session"].split("/")[-1]
        usuario = {"cpf": "111.111.111-11"}
        lista_infos = []

        # Pra quando quiser gravar o valor da nota no banco de dados
        # print("dados", dados['queryResult']['parameters']['number']);
        info_dao = InfoDAO()
        for inf in global_dados[sessao]["infos"]:
            busca = await info_dao.consultar(inf)
            if busca:
                from Model.Info import Info
                info_dict = busca[0]
                info = Info(
                    id=info_dict["id"],
                    nome=info_dict["nome"],
                    descricao=info_dict["descricao"],
                    status=info_dict["status"],
                    url_imagem=info_dict["url_imagem"]
                )
                lista_infos.append(info)

        chamado = LogInfo(0, usuario, "", lista_infos)
        await chamado.gravar()

        resposta = {"fulfillmentMessages": []}
        mensagem_final = [
            "Chegamos ao fim do atendimento. \n",
            "Obrigado pela avaliação, espero ter sido útil."
        ]
        if origem:
            resposta["fulfillmentMessages"].append({
                "text": {"text": mensagem_final}
            })
        else:
            resposta["fulfillmentMessages"].append({
                "payload": {
                    "richContent": [[{
                        "type": "description",
                        "title": "",
                        "text": mensagem_final
                    }]]
                }
            })

        return resposta
