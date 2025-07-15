# app/__init__.py

from flask import Flask
from dotenv import load_dotenv

def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.secret_key = "your-secret-key"  # Use os.environ.get(...) in production

    # Import routes and register blueprints
    from app.routes import main, client_bp
    app.register_blueprint(main)
    app.register_blueprint(client_bp)

    return app
