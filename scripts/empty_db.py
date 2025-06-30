from mods.database import drop_table

if __name__ == "__main__":
    print("🔍 Dropping all tables...")
    drop_table()
    print("✅ All tables dropped successfully.")
    print("🔄 Database is now empty.")