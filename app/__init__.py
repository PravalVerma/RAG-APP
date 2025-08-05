from flask import Flask
from app.routes.upload import upload_bp
from app.routes.ask import ask_bp
from app.routes.documents import documents_bp
from app.routes.query import query_bp
from app.routes.home import home_bp



def create_app():
    app = Flask(__name__)
    app.config["UPLOAD_FOLDER"] = "uploads"
    app.secret_key = "supersecret"
    app.register_blueprint(upload_bp)
    app.register_blueprint(ask_bp)
    app.register_blueprint(documents_bp)
    app.register_blueprint(query_bp)
    app.register_blueprint(home_bp)

    return app



