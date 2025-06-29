import psycopg2
import sys
from pgvector.psycopg2 import register_vector

from mods.env import DB_NAME, DB_USER, DB_PASS, DB_HOST, DB_PORT, EMBEDDING_DIMENSION

TABLE_QUERY = f"""
CREATE TABLE IF NOT EXISTS movie_embeddings (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    url TEXT,
    title_embedding VECTOR({EMBEDDING_DIMENSION}) NOT NULL,
    desc_embedding VECTOR({EMBEDDING_DIMENSION}) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
"""

TABLE_QUERY_JSON = f"""
CREATE TABLE IF NOT EXISTS movie_json_embeddings (
    id SERIAL PRIMARY KEY,
    content JSONB,
    embedding VECTOR({EMBEDDING_DIMENSION}) NOT NULL
);"""

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
        register_vector(conn)
        return conn
    except Exception as e:
        print(f"❌ Error connecting to the database: {e}")
        sys.exit(1)

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

def create_table():
    try:
        conn = create_connection()
        with conn.cursor() as cur:
            cur.execute(TABLE_QUERY)
            cur.execute(TABLE_QUERY_JSON)
            cur.close()
        print("✅ Table 'movie_embeddings', 'movie_json_embeddings' exists.")
        return True
    except Exception as e:
        print(f"Error checking table existence: {e}")
        return False