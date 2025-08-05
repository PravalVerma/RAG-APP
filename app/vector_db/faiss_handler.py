# Indexing and querying FAISS
import os
import faiss
import numpy as np
import pickle
from typing import Union

# Constants
INDEX_DIR = "faiss_index"
INDEX_PATH = os.path.join(INDEX_DIR, "index.bin")
META_PATH = os.path.join(INDEX_DIR, "metadata.pkl")
DIMENSION = 1536  # Set to match your embedding dimension (Mistral Embed)

# Ensure directory exists
os.makedirs(INDEX_DIR, exist_ok=True)

# Global variables
index: Union[faiss.IndexFlatL2, None] = None
metadata: list = []

# Initialize new FAISS index
def init_faiss(dimension=DIMENSION):
    global index
    index = faiss.IndexFlatL2(dimension)

# Load existing index and metadata
def load_index():
    global index, metadata
    if os.path.exists(INDEX_PATH) and os.path.exists(META_PATH):
        index = faiss.read_index(INDEX_PATH)
        with open(META_PATH, "rb") as f:
            metadata = pickle.load(f)
        print("✅ FAISS index and metadata loaded")
    else:
        init_faiss()
        metadata.clear()
        print("🆕 Created new FAISS index")

# Save index and metadata
def save_index():
    if index is not None:
        faiss.write_index(index, INDEX_PATH)
        with open(META_PATH, "wb") as f:
            pickle.dump(metadata, f)
        print("💾 FAISS index saved")

# Store embedded vectors into FAISS
def store_in_faiss(embedded_data):
    global index, metadata
    if index is None:
        raise RuntimeError("❌ FAISS index not initialized. Call init_faiss() or load_index() first.")

    vectors = [np.array(vec).astype("float32") for vec, _, _ in embedded_data]
    chunks = [(chunk, doc_name) for _, chunk, doc_name in embedded_data]

    if not vectors:
        raise ValueError("❌ No vectors to store in FAISS.")

    index.add(np.vstack(vectors))
    metadata.extend(chunks)
    save_index()

# Search top_k similar chunks
def search_faiss(query_vector, top_k=5):
    global index, metadata
    if index is None:
        raise RuntimeError("❌ FAISS index not initialized. Call init_faiss() or load_index() first.")

    query_vector = np.array(query_vector).astype("float32").reshape(1, -1)
    distances, indices = index.search(query_vector, top_k)
    return [metadata[i] for i in indices[0] if i < len(metadata)]

def delete_chunks_by_filename(filename: str):
    global metadata, index

    if index is None:
        raise RuntimeError("❌ FAISS index not initialized.")

    # Filter metadata
    filtered_metadata = [(chunk, doc_name) for chunk, doc_name in metadata if doc_name != filename]

    if len(filtered_metadata) == len(metadata):
        return False  # Nothing deleted

    # Rebuild index
    from app.embeddings.embedder import embed_texts  # Now this works
    texts = [chunk for chunk, _ in filtered_metadata]
    embeddings = embed_texts(texts)

    new_index = faiss.IndexFlatL2(len(embeddings[0])) if embeddings else faiss.IndexFlatL2(1536)
    if embeddings:
        new_index.add(np.array(embeddings).astype("float32"))

    # Save new index and metadata
    index = new_index
    metadata = filtered_metadata
    save_index()
    return True
