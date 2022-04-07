import os
import re
from os import path

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

#from flask_login import LoginManager


from .views import views
from .auth import auth


from .models import db, User

DB_NAME = "database.db"


def create_app():
    app = Flask(__name__, static_folder='./first-react-flask-app/build', static_url_path='/')
    CORS(app)
    app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET')
    jwt = JWTManager(app)
    uri = 'postgres://mcxdtmlyawwruz:cae33a97a8b9318e0d47869d43997abad73e527fb9e6fd2a9c9e9980acc195c4@ec2-52-73-155-171.compute-1.amazonaws.com:5432/d609nk86b17jko'#f'sqlite:///{DB_NAME}'
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    create_database(app)
    
    return app



def create_database(app):
    if not path.exists('web/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
