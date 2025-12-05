import os
from flask import Flask
from backend.app.extensions import db
from backend.app.api.auth.routes import bp as auth_bp
from backend.app.api.users.routes import bp as users_bp
try:
    from flask_cors import CORS
except ImportError:
    CORS = None

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")
    db.init_db()
    if CORS:
        origins = os.getenv("CORS_ORIGINS", "*")
        CORS(app,
             resources={r"/*": {"origins": origins}},
             expose_headers=["Content-Type", "Authorization"],
             allow_headers=["Content-Type", "Authorization"],
             methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    return app
