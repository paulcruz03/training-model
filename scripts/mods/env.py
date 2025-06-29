import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env from the project root (one level above scripts/)
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Load variables from .env
DB_NAME = os.getenv("POSTGRES_DB", "vector_db")
DB_USER = os.getenv("POSTGRES_USER", "user")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "password")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DATA_DIR = os.getenv("DATA_DIR", "rawdata/movies_metadata.csv")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
