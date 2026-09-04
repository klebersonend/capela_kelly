import os
import logging
from contextlib import contextmanager
import psycopg2
from psycopg2.extras import RealDictCursor

logger = logging.getLogger(__name__)

def get_database_url():
    url = os.environ.get("DATABASE_URL", "")
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    return url

@contextmanager
def get_db_connection():
    """
    Context manager seguro para conexões com o PostgreSQL.
    Garante rollback em caso de exceção e fechamento da conexão.
    """
    db_url = get_database_url()
    if not db_url:
        raise ValueError("DATABASE_URL não configurada nas variáveis de ambiente.")
    
    conn = psycopg2.connect(db_url, sslmode="require" if "render.com" in db_url else "prefer")
    try:
        yield conn
    except Exception as e:
        conn.rollback()
        logger.error(f"Erro em transação de banco de dados: {e}")
        raise
    finally:
        conn.close()

@contextmanager
def get_db_cursor(commit=False):
    """
    Context manager seguro para cursores de banco de dados.
    Garante retorno de dicts (RealDictCursor) e commit automático se solicitado.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            yield cursor
            if commit:
                conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
