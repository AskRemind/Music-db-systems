from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

bp = Blueprint('users', __name__)

@bp.route('/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(Email=data['email']).first():
        return jsonify({"error": "Email already registered"}), 400
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(Name=data['name'], Email=data['email'], PasswordHash=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully!"}), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(Email=data['email']).first()
    if not user or not check_password_hash(user.PasswordHash, data['password']):
        return jsonify({"error": "Invalid credentials"}), 401
    return jsonify({"message": "Login successful", "user_id": user.UserID}), 200

@bp.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.json
    user = User.query.filter_by(Email=data['email']).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    user.PasswordHash = generate_password_hash(data['new_password'], method='sha256')
    db.session.commit()
    return jsonify({"message": "Password reset successful!"}), 200
