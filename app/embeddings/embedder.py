
import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")  # ✅ Use generic name

EMBEDDING_MODEL = "openrouter/mistral-embed"

def get_embedding(text):
    url = "https://openrouter.ai/api/v1/embeddings"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": EMBEDDING_MODEL,
        "input": text
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["data"][0]["embedding"]

def embed_texts(chunks):
    """Returns a list of embeddings for input texts (chunks)"""
    embeddings = []
    for chunk in chunks:
        try:
            embedding = get_embedding(chunk)
            embeddings.append(embedding)
        except Exception as e:
            print(f"⚠️ Error embedding chunk: {e}")
    return embeddings

