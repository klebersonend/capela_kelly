import os
import sys
import logging
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv

# Carrega .env se presente
load_dotenv()

# Ajuste de path para importação
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.db import get_db_cursor

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

INITIAL_USERS = [
    {
        "username": "end",
        "env_var": "INITIAL_PASSWORD_END",
        "default_pass": "xpto$76",
        "nome_completo": "Administrador End",
        "perfil": "Administrador"
    },
    {
        "username": "kelly",
        "env_var": "INITIAL_PASSWORD_KELLY",
        "default_pass": "xpto$83",
        "nome_completo": "Kelly Santana",
        "perfil": "Capelã"
    }
]

def init_database():
    """
    Cria as tabelas necessárias e inicializa os usuários com hash scrypt seguro.
    As senhas são lidas das variáveis de ambiente para evitar exposição de segredos.
    Totalmente parametrizado contra SQL Injection.
    """
    logger.info("Iniciando verificação e criação da estrutura do banco de dados...")

    create_table_query = """
    CREATE TABLE IF NOT EXISTS usuarios (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        nome_completo VARCHAR(100) NOT NULL,
        perfil VARCHAR(50) NOT NULL,
        criado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        ultimo_acesso TIMESTAMP WITH TIME ZONE
    );
    """

    with get_db_cursor(commit=True) as cursor:
        cursor.execute(create_table_query)
        logger.info("Tabela 'usuarios' verificada/criada com sucesso.")

        for user_data in INITIAL_USERS:
            # Verifica se o usuário já existe
            cursor.execute("SELECT id FROM usuarios WHERE username = %s;", (user_data["username"],))
            existing = cursor.fetchone()

            password_raw = os.environ.get(user_data["env_var"], user_data["default_pass"])
            password_hash = generate_password_hash(password_raw, method="scrypt")

            if not existing:
                insert_query = """
                INSERT INTO usuarios (username, password_hash, nome_completo, perfil)
                VALUES (%s, %s, %s, %s);
                """
                cursor.execute(
                    insert_query,
                    (user_data["username"], password_hash, user_data["nome_completo"], user_data["perfil"])
                )
                logger.info(f"Usuário '{user_data['username']}' inserido com sucesso (hash seguro scrypt).")
            else:
                # Se o usuário já existe, não sobrescreve a senha caso já tenha sido definida
                pass

    logger.info("Inicialização do banco concluída com sucesso!")

if __name__ == "__main__":
    init_database()
