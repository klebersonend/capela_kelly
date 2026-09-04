import os
import sqlite3
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

def is_sqlite():
    url = get_database_url()
    return not url or url.startswith("sqlite")

class SQLiteDictCursor:
    """Wrapper para SQLite simular cursor psycopg2 com suporte a RealDictCursor e queries %s"""
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()

    def execute(self, query, params=None):
        # Converte placeholders %s do Postgres para ? do SQLite se necessário
        sqlite_query = query.replace("%s", "?")
        sqlite_query = sqlite_query.replace("TIMESTAMP WITH TIME ZONE", "TIMESTAMP")
        sqlite_query = sqlite_query.replace("SERIAL PRIMARY KEY", "INTEGER PRIMARY KEY AUTOINCREMENT")
        if params is None:
            return self.cursor.execute(sqlite_query)
        return self.cursor.execute(sqlite_query, params)

    def fetchone(self):
        row = self.cursor.fetchone()
        if row is None:
            return None
        return dict(row)

    def fetchall(self):
        rows = self.cursor.fetchall()
        return [dict(r) for r in rows]

    def close(self):
        self.cursor.close()

@contextmanager
def get_db_cursor(commit=False):
    """
    Context manager seguro e transparente.
    Conecta ao PostgreSQL do Render ou usa SQLite local como fallback de desenvolvimento.
    """
    db_url = get_database_url()
    
    # Tentativa com PostgreSQL
    if db_url and not db_url.startswith("sqlite"):
        try:
            conn = psycopg2.connect(db_url)
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
                conn.close()
            return
        except Exception as e:
            logger.warning(f"Conexão externa com PostgreSQL indisponível ({e}). Utilizando banco local SQLite.")

    # Fallback transparente para SQLite local (desenvolvimento offline)
    local_db_path = os.path.join(os.path.dirname(__file__), "..", "local_dev.db")
    conn = sqlite3.connect(local_db_path)
    conn.row_factory = sqlite3.Row
    cursor = SQLiteDictCursor(conn)
    try:
        yield cursor
        if commit:
            conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()
