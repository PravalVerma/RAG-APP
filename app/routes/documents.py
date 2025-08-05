# app/routes/documents.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db.mongo_handler import get_all_documents, delete_document_metadata
from app.vector_db.faiss_handler import delete_chunks_by_filename
import os

UPLOAD_FOLDER = os.path.join("app", "uploads")

documents_bp = Blueprint('documents', __name__)

@documents_bp.route('/documents', methods=['GET'])
def list_documents():
    documents = get_all_documents()
    return render_template("documents.html", documents=documents)

@documents_bp.route('/documents/delete/<filename>', methods=['POST'])
def delete_document(filename):
    # Delete from FAISS and metadata
    chunks_deleted = delete_chunks_by_filename(filename)
    delete_document_metadata(filename)

    # Delete the uploaded file
    pdf_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(pdf_path):
        os.remove(pdf_path)

    flash(f"{filename} deleted successfully!" if chunks_deleted else f"{filename} not found in vector store.")
    return redirect(url_for('documents.list_documents'))
