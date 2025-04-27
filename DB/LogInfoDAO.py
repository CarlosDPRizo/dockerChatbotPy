import asyncio
from DB.Conexao import conectar  # Importa a função de conexão já criada

class LogInfoDAO:
    async def init(self):
        try:
            conexao = await conectar()
            sql = """
                CREATE TABLE IF NOT EXISTS log_info (
                    fk_info_id INT NOT NULL,
                    fk_usu_cpf VARCHAR(14) NOT NULL,
                    data VARCHAR(10) NOT NULL,
                    CONSTRAINT fk_info_log FOREIGN KEY (fk_info_id) REFERENCES info(id),
                    CONSTRAINT fk_usuario_log FOREIGN KEY (fk_usu_cpf) REFERENCES usuario(pk_usu_cpf)
                )
            """

            async with conexao.cursor() as cursor:
                await cursor.execute(sql)
            await conexao.commit()

            print("Tabela log_info iniciada com sucesso!")
        except Exception as erro:
            print(f"Não foi possível iniciar a tabela log_info: {erro}")
        finally:
            conexao.close()

    async def gravar(self, log_info):
        from Model.LogInfo import LogInfo
        
        if isinstance(log_info, LogInfo):
            conexao = await conectar()

            try:
                async with conexao.cursor() as cursor:
                    await conexao.begin()  # Inicia a transação
                    data = asyncio.get_event_loop().time()  # Obtém a data atual

                    for info in log_info.infos:
                        sql_log_infos = """
                            INSERT INTO log_info (fk_info_id, fk_usu_cpf, data)
                            VALUES (%s, %s, %s)
                        """
                        
                        parametros = (info.id, log_info.usuario["cpf"], data)
                        await cursor.execute(sql_log_infos, parametros)

                    await conexao.commit()  # Confirma a transação
            except Exception as erro:
                await conexao.rollback()  # Reverte a transação em caso de erro
                print(f"Erro ao gravar log_info: {erro}")
            finally:
                conexao.close()
