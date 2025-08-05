# Splits documents into chunks
import fitz  # PyMuPDF
import os
from app.embeddings.embedder import embed_and_store
from app.db.mongo_handler import store_metadata

CHUNK_SIZE = 500  # characters
CHUNK_OVERLAP = 100



def extract_text_from_pdf(filepath):
    text = ""
    with fitz.open(filepath) as doc:
        for page in doc:
            text += page.get_text()
    return text

def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def process_and_store_pdf(filepath, doc_name):
    print(f"📄 Processing: {doc_name}")
    
    text = extract_text_from_pdf(filepath)
    chunks = chunk_text(text)

    metadata = {
        "doc_name": doc_name,
        "num_chunks": len(chunks),
        "filepath": filepath
    }

    store_metadata(metadata)  # Save in MongoDB
    embed_and_store(chunks, doc_name)  # Embed and store in FAISS

    print(f"Extracted {len(chunks)} chunks from {doc_name}")
