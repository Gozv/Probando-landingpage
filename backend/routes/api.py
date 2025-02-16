from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from backend.models import db, Project, Message
from backend.utils.crypto import encrypt_data

api = Blueprint('api', __name__)

@api.route('/projects', methods=['GET'])
def get_projects():
    projects = Project.query.all()
    return jsonify([{
        'id': p.id,
        'title': p.title,
        'technologies': p.technologies
    } for p in projects])

@api.route('/contact', methods=['POST'])
def send_message():
    data = request.json
    new_message = Message(
        name=data['name'],
        email=data['email'],
        content=encrypt_data(data['message'])
    )
    db.session.add(new_message)
    db.session.commit()
    return jsonify({'message': 'Message received'}), 201