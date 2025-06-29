import sys
from mods.database import database_exists, ensure_pgvector_enabled, create_table, DB_NAME
from mods.parsing import load_csv
from mods.modeling import get_embeddings, insert_embedding

if __name__ == "__main__":
    print(f"🔍 Checking if database '{DB_NAME}' exists...")
    if database_exists(DB_NAME) is False:
        print(f"❌ Database '{DB_NAME}' does not exist.")
        sys.exit(1)
    
    print(f"✅ Database '{DB_NAME}' exists.")
    ensure_pgvector_enabled()
    if create_table() is False:
        print("❌ Failed to create tables.")
        sys.exit(1)

    df = load_csv()
    print(df.head(1))  # Show first few rows
    get_embeddings("sample")

    
