from flask import Blueprint, request, jsonify
from app.embeddings.embedder import get_embedding
from app.vector_db.faiss_handler import search_faiss
from app.services.rag_llm import generate_answer

ask_bp = Blueprint('ask', __name__)

@ask_bp.route("/ask", methods=["POST"])
def ask_question():
    data = request.get_json()
    question = data.get("question")

    if not question:
        return jsonify({"error": "Question is required"}), 400

    query_embedding = get_embedding(question)
    top_chunks = search_faiss(query_embedding, top_k=5)

    context = "\n\n".join([chunk for chunk, _ in top_chunks])
    answer = generate_answer(question, context)

    return jsonify({"answer": answer, "chunks_used": top_chunks})
