import os
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
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://nitpxcpibpzvaf:05b8448c48217213cfd737eb39680aa026482b04d545d1ad5af25495bc2b35e1@ec2-52-73-155-171.compute-1.amazonaws.com:5432/db5e2o0u0asnj8'#f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    create_database(app)
    
    return app



def create_database(app):
    if not path.exists('web/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
