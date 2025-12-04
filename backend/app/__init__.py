import os
from flask import Flask
from backend.app.extensions import db
from backend.app.api.auth.routes import bp as auth_bp

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")
    db.init_db()
    app.register_blueprint(auth_bp)
    return app
