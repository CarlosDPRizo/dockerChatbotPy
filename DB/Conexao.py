import os
import aiomysql
from dotenv import load_dotenv

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

pool_conexoes = None

async def conectar():
    global pool_conexoes

    if pool_conexoes:
        # Retorna uma conexão existente do pool
        return await pool_conexoes.acquire()
    else:
        # Cria um novo pool de conexões
        pool_conexoes = await aiomysql.create_pool(
            host=os.getenv("DB_HOST", "db"),
            user=os.getenv("DB_USER", "user"),
            password=os.getenv("DB_PASSWORD", "passwd"),
            db=os.getenv("DB_DATABASE", "chatbot"),
            minsize=1,         # Mínimo de conexões
            maxsize=50,        # Máximo de conexões no pool
            autocommit=True    # Autocommit habilitado
        )
        # Retorna uma conexão do pool
        return await pool_conexoes.acquire()
