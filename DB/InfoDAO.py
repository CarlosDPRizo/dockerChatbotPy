import aiomysql
from DB.Conexao import conectar  # Função conectar previamente criada
import warnings
warnings.filterwarnings("ignore", message="Table '.*' already exists")  # 👈 Ignora avisos de tabela existente
class InfoDAO:    
    def __init__(self):
        self.init()  # Método síncrono

    def init(self):
        # Código de inicialização síncrono
        pass

    async def init(self):
        try:
            # Cria a tabela info caso ela não exista
            sql = """
                CREATE TABLE IF NOT EXISTS info (
                    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                    nome VARCHAR(100) NOT NULL,
                    descricao VARCHAR(200) NOT NULL,
                    status VARCHAR(100) NOT NULL,
                    urlImagem VARCHAR(500) NOT NULL
                )
            """
            conexao = await conectar()
            async with conexao.cursor() as cursor:
                await cursor.execute(sql)
            await conexao.commit()
            print("Tabela info iniciada com sucesso!")
        except Exception as error:
            print(f"Não foi possível iniciar a tabela info: {error}")

    async def gravar(self, info):
        from Model.Info import Info
        
        if isinstance(info, Info):
            sql = """
                INSERT INTO info (nome, descricao, status, urlImagem)
                VALUES (%s, %s, %s, %s)
            """
            parametros = (info.nome, info.descricao, info.status, info.urlImagem)

            conexao = await conectar()
            async with conexao.cursor() as cursor:
                await cursor.execute(sql, parametros)
                await conexao.commit()
                info.id = cursor.lastrowid

    async def alterar(self, info):
        from Model.Info import Info
        
        if isinstance(info, Info):
            sql = """
                UPDATE info
                SET nome = %s, descricao = %s, status = %s, urlImagem = %s
                WHERE id = %s
            """
            parametros = (info.nome, info.descricao, info.status, info.urlImagem, info.id)

            conexao = await conectar()
            async with conexao.cursor() as cursor:
                await cursor.execute(sql, parametros)
                await conexao.commit()

    async def excluir(self, info):
        from Model.Info import Info
        
        if isinstance(info, Info):
            sql = "DELETE FROM info WHERE id = %s"
            parametros = (info.id,)

            conexao = await conectar()
            async with conexao.cursor() as cursor:
                await cursor.execute(sql, parametros)
                await conexao.commit()

    async def consultar(self, termo_busca=''):
        sql = """
            SELECT *
            FROM info
            WHERE descricao LIKE %s
            ORDER BY nome
        """
        parametros = (f"%{termo_busca or ''}%",)

        conexao = await conectar()
        print("Conexão estabelecida:", conexao)

        async with conexao.cursor(aiomysql.DictCursor) as cursor:
            print("SQL:", sql)
            print("Parâmetros:", parametros)

            await cursor.execute(sql, parametros)
            registros = await cursor.fetchall()

            print('registros:', registros)
        lista_servicos = []
        for registro in registros:
            from Model.Info import Info
            
            info = Info(
                id=registro["id"],
                nome=registro["nome"],
                descricao=registro["descricao"],
                status=registro["status"],
                url_imagem=registro["urlImagem"]
            )
            
            lista_servicos.append(info.to_json())
            
        return lista_servicos
