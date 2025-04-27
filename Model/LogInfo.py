from DB.LogInfoDAO import LogInfoDAO  # Importa LogInfoDAO previamente adaptado

class LogInfo:
    def __init__(self, fk_info_id=0, usuario=None, data='', infos=None):
        self._fk_info_id = fk_info_id
        self._usuario = usuario if usuario else {"cpf": ""}
        self._data = data
        self._infos = infos if infos else []

    # Getters
    @property
    def fk_info_id(self):
        return self._fk_info_id

    @property
    def data(self):
        return self._data

    @property
    def usuario(self):
        return self._usuario

    @property
    def infos(self):
        return self._infos

    # Setters
    @fk_info_id.setter
    def fk_info_id(self, fk_info_id):
        self._fk_info_id = fk_info_id

    @data.setter
    def data(self, data):
        self._data = data

    @usuario.setter
    def usuario(self, usuario):
        self._usuario = usuario

    @infos.setter
    def infos(self, infos):
        self._infos = infos

    # Método to_json para converter para dicionário
    def to_json(self):
        return {
            "fk_info_id": self._fk_info_id,
            "data": self._data,
            "usuario": self._usuario,
            "infos": self._infos,
        }

    # Método assíncrono para gravar
    async def gravar(self):
        log_dao = LogInfoDAO()
        await log_dao.gravar(self)
