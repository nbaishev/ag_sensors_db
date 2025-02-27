from flask import (
    Blueprint, request, jsonify
)
from flask_jwt_extended import create_access_token, jwt_required
from werkzeug.security import check_password_hash, generate_password_hash

from app.database import db
from app.models import User
from app.utils import admin_required

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('POST',))
@jwt_required()
@admin_required
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    role = data.get("role", "user")

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "User already exists"}), 400

    new_user = User(
        username=username,
        password=generate_password_hash(password),
        role=role,
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered"}), 201


@bp.route('/login', methods=('POST',))
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=username)
    return jsonify({"access_token": access_token})
