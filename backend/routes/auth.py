from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from backend.models import db, User
import bcrypt

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({"error": "Missing credentials"}), 400

        user = User.query.filter_by(username=data['username']).first()
        if not user or not bcrypt.checkpw(data['password'].encode('utf-8'), user.password):
            return jsonify({"error": "Invalid credentials"}), 401

        access_token = create_access_token(identity=user.id)
        return jsonify({
            "access_token": access_token,
            "user_id": user.id
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500