from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from backend.models import db, Project, Message
from backend.utils.crypto import encrypt_data
import logging

api = Blueprint('api', __name__)

@api.route('/projects', methods=['GET'])
def get_projects():
    try:
        projects = Project.query.order_by(Project.created_at.desc()).all()
        return jsonify([{
            'id': p.id,
            'title': p.title,
            'technologies': p.technologies,
            'created_at': p.created_at.isoformat()
        } for p in projects]), 200
    except Exception as e:
        logging.error(f"Error getting projects: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@api.route('/contact', methods=['POST'])
@jwt_required()
def send_message():
    try:
        data = request.get_json()
        
        required_fields = ['name', 'email', 'message']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400
        
        new_message = Message(
            name=data['name'],
            email=data['email'],
            content=encrypt_data(data['message'])
        )
        
        db.session.add(new_message)
        db.session.commit()
        
        return jsonify({
            "message": "Message received successfully",
            "id": new_message.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error sending message: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500