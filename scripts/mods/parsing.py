import pandas as pd
import json
from pathlib import Path
from mods.env import DATA_DIR
from mods.modeling import insert_embedding

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

def process_csv(df: pd.DataFrame):
    """Parse the DataFrame into a list of dictionaries."""
    try:
        data = df.to_dict(orient='records')
        for entry in data:
            title = entry.get('title', '')
            description = entry.get('overview', '')
            url = entry.get('homepage', '')
            json_content = {"title": title, "description": description, "url": url} 
            json_string = json.dumps(json_content)
            if insert_embedding(title, description, url, json_string):
                print(f"✅ Entry '{title}' processed successfully.")
            else:
                print(f"❌ Failed to process entry '{title}'.")
        print("✅ CSV parsed successfully.")
    except Exception as e:
        print(f"❌ Error parsing CSV: {e}")