import numpy as np
from app.vector_db.faiss_handler import search_faiss
from app.embeddings.embedder import get_embedding

def get_relevant_chunks(question: str, top_k=5):
    """
    Given a question, returns top_k relevant (chunk, doc_name) tuples.
    """
    query_embedding = get_embedding(question)
    results = search_faiss(query_embedding, top_k=top_k)
    return results
