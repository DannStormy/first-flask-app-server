from flask import Blueprint, jsonify, request, flash
from flask_login import current_user
from flask_jwt_extended import create_access_token
#from flask_cors import CORS, cross

#from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import true
from werkzeug.security import generate_password_hash, check_password_hash

from .models import User
from .models import db

auth = Blueprint('auth', __name__)


@auth.route('/api/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data['username']
        password = data['password']

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                access_token = create_access_token(identity=username)
                print('Logged in Successfully')
                return jsonify(access_token=access_token, username=username)
            else:
                print('Incorrect password')
        else:
            print('User does not exist')
            print(user)
            return 'Done', 201


@auth.route('/api/logout')
def logout():
    # logout_user()
    return "<p>This is the logout page</p>"


@auth.route('/api/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        # get json data from post request
        data = request.get_json()
        # split data
        firstName = data['firstName']
        lastName = data['lastName']
        username = data['username']
        email = data['email']
        password = data['password']
        user = User.query.filter_by(email=email).first()
        oldUser = User.query.filter_by(username=username).first()
        if user:
            print('Email exists, please login if you already have an account')
            return "Email exists", 500
        elif oldUser:
            print("Username already exists")
            return "Username exists", 500
        # store new_user with data
        else:
            print(username)
            new_user = User(email=email, firstName=firstName,
                            lastName=lastName, username=username,
                            password=generate_password_hash(password, method='pbkdf2:sha256'))
        # add user
            db.session.add(new_user)
            db.session.commit()
            print("New User")
    return {"Signed-up": True}
