## TODO: Change to other embedding model
import openai
from mods.database import create_connection
from mods.env import OPENAI_API_KEY

client = openai.OpenAI(api_key=OPENAI_API_KEY)

def get_embeddings(text):
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=text,
        encoding_format="float"
    )
    embedding = response['data'][0]['embedding']
    return embedding

def insert_embedding(title, description, url, tokens, embedding):
    try:
        conn = create_connection()
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO movie_embeddings (title, description, url, tokens, embedding) VALUES (%s, %s, %s, %s, %s)",
                (title, description, url, tokens, embedding)
            )
            conn.commit()
        print("✅ Entry %s: Embedding inserted successfully.", title)
        return True
    except Exception as e:
        print(f"Error inserting embedding: {e}")
        return False