import os
from flask import Blueprint, request, render_template, redirect, flash, url_for
from werkzeug.utils import secure_filename
from app.services.chunker import process_and_store_pdf

upload_bp = Blueprint('upload', __name__)

UPLOAD_FOLDER = os.path.join("app", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files.get("file")

        if not file or not file.filename:
            flash("❌ No file selected.")
            return redirect(request.url)

        filename = file.filename

        if not allowed_file(filename):
            flash("❌ Only PDF files are allowed.")
            return redirect(request.url)

        safe_filename = secure_filename(filename)
        filepath = os.path.join(UPLOAD_FOLDER, safe_filename)
        file.save(filepath)

        # Process file: chunk, embed, store
        process_and_store_pdf(filepath, safe_filename)

        flash("✅ File uploaded and processed successfully!")
        return redirect(url_for("upload.upload_file"))

    return render_template("upload.html")
