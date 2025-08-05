# Handles user queries and RAG pipeline
from flask import Blueprint, request, render_template
from app.embeddings.embedder import get_embedding
from app.vector_db.faiss_handler import search_faiss
from app.llm.openrouter import query_openrouter

query_bp = Blueprint('query', __name__)

@query_bp.route("/ask", methods=["GET", "POST"])
def ask():
    answer = None
    if request.method == "POST":
        question = request.form["question"]
        query_vector = get_embedding(question)
        relevant_chunks = search_faiss(query_vector)

        context = "\n".join([chunk[0] for chunk in relevant_chunks])  # (chunk_text, doc_name)
        answer = query_openrouter(question, context)

    return render_template("query.html", answer=answer)
