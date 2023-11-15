from datetime import timedelta

from flask import Flask
from flask_jwt_extended import JWTManager

from app.config import config
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_pymongo import PyMongo

from routes.api import main_bp


# Set up Flask-login
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

# Setup CSRF
csrf = CSRFProtect()

# Security Measures dict initially None
security = None

db = PyMongo()

def create_app(config_name):
    """For to use dynamic environment"""
    global security
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    app.config['JWT_SECRET_KEY'] = 'your_secret_key123'  # TODO : move this in .env
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

    jwt = JWTManager(app)

    db.init_app(app)
    login_manager.init_app(app)

    csrf.init_app(app)

    app.register_blueprint(main_bp)

    return app