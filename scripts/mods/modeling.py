from mods.database import create_connection
from mods.env import MODEL  # Import the model from env.py

# Load the tokenizer and model from Hugging Face


def get_embeddings(text: str):
    try:
        embedding = MODEL.encode(text).tolist()
        return embedding
    except Exception as e:
        print(f"Error getting embeddings: {e}")
        return None

def insert_embedding(title, description, url, json_content):
    try:
        title_embedding = get_embeddings(title)
        desc_embedding = get_embeddings(description)
        content_embedding = get_embeddings(json_content)
        conn = create_connection()
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO movie_embeddings (title, description, url, title_embedding, desc_embedding) VALUES (%s, %s, %s, %s, %s)",
                (title, description, url, title_embedding, desc_embedding)
            )
            cur.execute(
                "INSERT INTO movie_json_embeddings (content, embedding) VALUES (%s, %s)",
                (json_content, content_embedding)
            )
            conn.commit()
        print("✅ Entry %s: Embedding inserted successfully.", title)
        return True
    except Exception as e:
        print(f"Error inserting embedding: {e}")
        return False

def get_entry_by_embedding(query, top_k: int = 5):
    query_embedding = MODEL.encode(query).tolist()
    conn = create_connection()
    results = []
    with conn.cursor() as cur:
        cur.execute(f"""
            SELECT content, 1 - (embedding <=> %s) AS similarity
            FROM movie_json_embeddings
            ORDER BY similarity DESC
            LIMIT %s;
        """, (query_embedding, top_k))

        fetched_results = cur.fetchall()
        for content, similarity in fetched_results:
            results.append({"content": content, "similarity": similarity})
        
        return results