from app import create_app
import sys
from app.vector_db.faiss_handler import init_faiss
from app.vector_db.faiss_handler import load_index


sys.path.append(".")

app = create_app()
init_faiss()     
load_index() 


if __name__ == "__main__":
    app.run(debug=True)

