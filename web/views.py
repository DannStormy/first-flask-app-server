from audioop import cross
from calendar import c
import json

from flask import Blueprint, send_from_directory
#from flask_cors import CORS, cross_origin
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required


from .models import Note, User, db

views = Blueprint('views', __name__)





@views.route('/api/addnote', methods=['GET', 'POST'])
@jwt_required()
def add_note():
    current_user = get_jwt_identity()
    print("Current user is " + current_user)
    print(User.query.filter_by(username=current_user).first())
    if request.method == "POST":
        data = request.get_json()
        note = data['note']
        can_view_records = data['status']
        if len(note) < 1:
            return jsonify(error="note too short")
        else:
            new_note = Note(
                data=note, can_view_records=can_view_records, owner=current_user)
            db.session.add(new_note)
            db.session.commit()
            print("Note added!")
        return 'Done', 201


@views.route('/api/notesfeed', methods=['GET', 'POST'])
#@jwt_required()
def all_notes():
    if request.method == "GET":
        notes = Note.query.order_by(Note.date)
        return jsonify(notes)


@views.route('/api/mynotes', methods=['GET', 'POST'])
@jwt_required()
def personal_notes():
    current_user = get_jwt_identity()
    if request.method == "GET":
        notes = Note.query.filter_by(user_id=current_user).all()
        return jsonify(notes)


@views.route('/api/delete-note', methods=['POST'])
@jwt_required()
def delete_note():
    current_user = get_jwt_identity()
    data = request.get_json()
    print(data)
    note_id = data['noteid']
    db_note = Note.query.get(note_id)
    print(db_note.id)
    if current_user:
        if note_id == db_note.id:
            db.session.delete(db_note)
            db.session.commit()
            return jsonify({"Deleted": True})
