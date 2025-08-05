# app/vector_db/mongo_connection.py

from pymongo import MongoClient

# Connect to local MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Use database "rag_app" and collection "metadata"
db = client["rag_app"]
metadata_collection = db["metadata"]
