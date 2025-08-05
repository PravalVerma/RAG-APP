from pymongo import MongoClient
from datetime import datetime
from app.vector_db.mongo_connection import metadata_collection


# MongoDB Config
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "rag_app"
COLLECTION_NAME = "documents"

# MongoDB Client and Collection
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
metadata_collection = db[COLLECTION_NAME]


# Store document metadata
def store_metadata(filename, chunks):
    metadata = {
        "doc_name": filename,
        "timestamp": datetime.now().isoformat(),
        "num_chunks": len(chunks)
    }
    metadata_collection.insert_one(metadata)
    print(f"🗃️ Stored metadata for {filename}")

# Retrieve all metadata records
def get_all_metadata():
    return list(metadata_collection.find({}, {"_id": 0}))

# Retrieve basic list of documents (used in UI)
def get_all_documents():
    return list(metadata_collection.find({}, {"_id": 0, "doc_name": 1, "timestamp": 1}))

def delete_document_metadata(filename: str):
    metadata_collection.delete_one({"filename": filename})
