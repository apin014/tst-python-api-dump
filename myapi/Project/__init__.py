from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager
)
from datetime import timedelta
import os, dotenv

dotenv.load_dotenv('..\.env')

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_TOKEN_LOCATION'] = ['cookies', 'headers']
    app.config['JWT_COOKIE_SECURE'] = False
    app.config['JWT_ACCESS_COOKIE_PATH'] = '/api/'
    app.config['JWT_COOKIE_CSRF_PROTECT'] = True
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URL')

    db.init_app(app)
    
    jwt = JWTManager(app)
    
    def unauthorized_token_callback(jwt_payload):
        return jsonify({'status':'unauthorized access', 'msg':'access token cannot be found'}), 401
    
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({'status':'expired token', 'msg':'access token has expired'}), 401
    
    jwt.unauthorized_loader(unauthorized_token_callback)
    jwt.expired_token_loader(expired_token_callback)

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    with app.app_context():
        db.create_all()

    return app