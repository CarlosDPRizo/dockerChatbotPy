from DB.InfoDAO import InfoDAO

def criar_messenger_card():
    return {
        "type": "info",
        "title": "",
        "subtitle": "",
        "image": {
            "src": {
                "rawUrl": ""
            }
        },
        "actionLink": ""
    }
# fim da função criar_messenger_card

def criar_custom_card():
    # Exibir nos ambientes padrões, tais como: ambiente de teste do DialogFlow, Slack, etc.
    return {
        "card": {
            "title": "",
            "subtitle": "",
            "imageUri": "",
            "buttons": [
                {
                    "text": "botão",
                    "postback": ""
                }
            ]
        }
    }
# fim da função criar_custom_card

async def obter_cards_infos(tipo_card="custom"):
    lista_cards_servicos = []
    info_dao = InfoDAO()
    infos = await info_dao.consultar()  # Método de consulta previamente adaptado

    for info in infos:
        if tipo_card == "custom":
            card = criar_custom_card()
            card["card"]["title"] = info["nome"]
            card["card"]["subtitle"] = f"Descrição: {info['descricao']}"
            card["card"]["imageUri"] = info["url_imagem"]
            card["card"]["buttons"][0]["postback"] = "https://guided-whale-initially.ngrok-free.app/info/home"
        else:
            card = criar_messenger_card()
            card["title"] = info["nome"]
            card["subtitle"] = f"Descrição: {info['descricao']}"
            card["image"]["src"]["rawUrl"] = info["url_imagem"]
            card["actionLink"] = "https://guided-whale-initially.ngrok-free.app/info/home"
    
        lista_cards_servicos.append(card)  # ← agora deve funcionar!

    return lista_cards_servicos
