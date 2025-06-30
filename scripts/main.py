import sys
from mods.database import database_exists, ensure_pgvector_enabled, create_table, DB_NAME
from mods.parsing import load_csv, process_csv

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
    process_csv(df)
    # results = get_entry_by_embedding("final destination")
    # print(f"🔍 Search results: {results}")
    
