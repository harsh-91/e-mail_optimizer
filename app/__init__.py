# app/__init__.py

from flask import Flask
from dotenv import load_dotenv

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'replace-this-secret'

    from .routes import main
    app.register_blueprint(main)

    return app
