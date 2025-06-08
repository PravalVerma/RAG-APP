import os

folders = [
    "app",
    "app/templates",
    "app/static",
    "app/routes",
    "app/services",
    "app/vector_db",
    "app/db"
]

files = {
    "app/__init__.py": "",
    "app/templates/upload.html": "<!-- File upload UI goes here -->",
    "app/routes/upload.py": "# Handles file upload and processing",
    "app/routes/query.py": "# Handles user queries and RAG pipeline",
    "app/routes/metadata.py": "# Shows document metadata",
    "app/services/chunker.py": "# Splits documents into chunks",
    "app/services/embedder.py": "# Converts text chunks into embeddings",
    "app/services/retriever.py": "# Retrieves top chunks from FAISS",
    "app/services/llm.py": "# Calls external LLM API",
    "app/vector_db/faiss_handler.py": "# Indexing and querying FAISS",
    "app/db/mongo_handler.py": "# MongoDB metadata operations",
    "Dockerfile": "# Docker build file for Flask app",
    "docker-compose.yml": "# Orchestrates Flask + MongoDB",
    "requirements.txt": "# Python dependencies",
    "README.md": "# Instructions for setup and usage"
}

# Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Create files
for path, content in files.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ Project scaffold created successfully.")
