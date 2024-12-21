from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
import random

bp = Blueprint('users', __name__)

def generate_custom_uid():
    part1 = random.randint(10, 99)
    part2 = random.randint(100, 999)
    part3 = random.randint(1000, 9999)
    return f"{part1}-{part2}-{part3}"

def generate_unique_custom_uid():
    while True:
        uid = generate_custom_uid()
        if not User.query.filter_by(UserID=uid).first():
            return uid

@bp.route('/register', methods=['POST'])
def register():
    data = request.json

    required_fields = ['FirstName', 'LastName', 'Email', 'Password', 'Gender']
    for field in required_fields:
        if field not in data or not data[field].strip():
            return jsonify({"error": f"Missing or empty field: {field}"}), 400

    if 'Age' in data and (not str(data['Age']).isdigit() or int(data['Age']) < 0):
        return jsonify({"error": "Invalid Age"}), 400

    if User.query.filter_by(Email=data['Email'].lower()).first():
        return jsonify({"error": "Email already exists"}), 409

    custom_uid = generate_unique_custom_uid()
    hashed_password = generate_password_hash(data['Password'], method='pbkdf2:sha256')

    new_user = User(
        UserID=custom_uid,
        FirstName=data['FirstName'],
        LastName=data['LastName'],
        Email=data['Email'].lower(),
        Age=int(data.get('Age', 0)),
        Country=data.get('Country', ''),
        Gender=data['Gender'],
        PasswordHash=hashed_password
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!", "user_id": custom_uid}), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.json

    if 'email' not in data or 'password' not in data:
        return jsonify({"error": "Email and password are required"}), 400

    user = User.query.filter_by(Email=data['email'].lower()).first()
    if not user or not check_password_hash(user.PasswordHash, data['password']):
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify({
        "message": "Login successful",
        "user": {
            "UserID": user.UserID,
            "FirstName": user.FirstName,
            "LastName": user.LastName,
            "Email": user.Email,
            "Age": user.Age,
            "Country": user.Country,
            "Gender": user.Gender
        }
    }), 200

@bp.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.json

    if 'email' not in data or 'new_password' not in data or 'old_password' not in data:
        return jsonify({"error": "Email, old password, and new password are required"}), 400

    user = User.query.filter_by(Email=data['email'].lower()).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    if not check_password_hash(user.PasswordHash, data['old_password']):
        return jsonify({"error": "Old password is incorrect"}), 403

    if len(data['new_password']) < 8:
        return jsonify({"error": "New password must be at least 8 characters long"}), 400

    user.PasswordHash = generate_password_hash(data['new_password'], method='pbkdf2:sha256')
    db.session.commit()

    return jsonify({"message": "Password reset successful!"}), 200


