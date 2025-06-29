import pandas as pd
from pathlib import Path
from mods.env import DATA_DIR

csv_path = Path(__file__).resolve().parent.parent.parent / DATA_DIR

def load_csv() -> pd.DataFrame:
    try:
        df = pd.read_csv(csv_path)
        print("✅ CSV loaded successfully:")
        return df
    except FileNotFoundError:
        print(f"❌ CSV not found at: {csv_path}")
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")