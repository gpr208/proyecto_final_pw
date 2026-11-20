import os
import psycopg2
from dotenv import load_dotenv

load_dotenv(override=True)

def obtener_conexion():
    try:
        return psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "5432")),
            dbname=os.getenv("DB_NAME", "proyecto_pw_bar"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD"),
            client_encoding="utf8"
        )
    except UnicodeDecodeError as e:
        raise RuntimeError(f"Error real de PostgreSQL: {e.object.decode('latin-1', errors='replace')}")