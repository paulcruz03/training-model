import psycopg2
import os
import sys
from dotenv import load_dotenv
from pathlib import Path

# Load .env from the project root (one level above scripts/)
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Load variables from .env
DB_NAME = os.getenv("POSTGRES_DB", "vector_db")
DB_USER = os.getenv("POSTGRES_USER", "user")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "password")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")

def create_connection():
    """Create a connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.autocommit = True
        return conn
    except Exception as e:
        print(f"❌ Error connecting to the database: {e}")
        sys.exit(1)

# Function definitions (same as before)
def database_exists(dbname):
    try:
        conn = create_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (dbname,))
            exists = cur.fetchone() is not None
        conn.close()
        return exists
    except Exception as e:
        print(f"Error checking database existence: {e}")
        sys.exit(1)

def ensure_pgvector_enabled():
    try:
        conn = create_connection()
        with conn.cursor() as cur:
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            print("✅ pgvector extension is enabled.")
        conn.close()
    except Exception as e:
        print(f"Error enabling pgvector extension: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print(f"🔍 Checking if database '{DB_NAME}' exists...")
    if database_exists(DB_NAME):
        print(f"✅ Database '{DB_NAME}' exists.")
        ensure_pgvector_enabled()
    else:
        print(f"❌ Database '{DB_NAME}' does not exist.")
        sys.exit(1)
