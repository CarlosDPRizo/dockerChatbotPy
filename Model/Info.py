from DB.InfoDAO import InfoDAO  # Importa InfoDAO previamente adaptado

class Info:
    def __init__(self, id=0, nome=None, descricao=None, status="", url_imagem=""):
        self._id = id
        self._nome = nome
        self._descricao = descricao
        self._status = status
        self._url_imagem = url_imagem

    # Getters e Setters
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, novo_id):
        self._id = novo_id

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, novo_nome):
        self._nome = novo_nome

    @property
    def descricao(self):
        return self._descricao

    @descricao.setter
    def descricao(self, nova_desc):
        self._descricao = nova_desc

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, novo_status):
        self._status = novo_status

    @property
    def url_imagem(self):
        return self._url_imagem

    @url_imagem.setter
    def url_imagem(self, nova_url):
        self._url_imagem = nova_url

    # Método para converter o objeto em JSON
    def to_json(self):
        return {
            "id": self._id,
            "nome": self._nome,
            "descricao": self._descricao,
            "status": self._status,
            "url_imagem": self._url_imagem
        }

    # Métodos assíncronos para integração com o DAO
    async def gravar(self):
        info_dao = InfoDAO()
        await info_dao.gravar(self)

    async def alterar(self):
        info_dao = InfoDAO()
        await info_dao.alterar(self)

    async def excluir(self):
        info_dao = InfoDAO()
        await info_dao.excluir(self)
