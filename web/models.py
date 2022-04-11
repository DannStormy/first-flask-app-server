import string
from xmlrpc.client import Boolean, boolean
from flask_login import UserMixin, current_user
from sqlalchemy import VARCHAR
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass

db = SQLAlchemy()


@dataclass
class Note(db.Model):
    id: int
    data: string
    owner = VARCHAR
    can_view_records: bool
    #user_id: int

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    can_view_records = db.Column(db.Boolean, default=False)
    owner = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


@dataclass
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(150))
    lastName = db.Column(db.String(150))
    username = db.Column(db.String(150), unique=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    notes = db.relationship('Note')
