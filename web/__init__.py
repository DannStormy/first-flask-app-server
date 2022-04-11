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
    #f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ixzcztnyllnnbl:e9cbb9e2b80a90bb1cb13370dd183a4ff17bac28fc66a0ced22e042e0fe88fc3@ec2-34-197-84-74.compute-1.amazonaws.com:5432/dbaqbn4bumsdbl'
    print(os.getenv('DATABASE_URL'))
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
