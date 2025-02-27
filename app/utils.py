from functools import wraps

from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity
from werkzeug.security import generate_password_hash

from app.database import db
from app.models import Controller, User


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        user = User.query.filter_by(username=current_user).first()

        if not user or user.role != 'admin':
            return jsonify({"error": "Access forbidden: Admins only"}), 403

        return fn(*args, **kwargs)

    return wrapper


def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get("X-API-KEY")
        if not api_key:
            return jsonify({"error": "API key is missing"}), 401

        sensor = Controller.query.filter_by(api_key=api_key).first()
        if not sensor:
            return jsonify({"error": "Invalid API key"}), 403

        return f(sensor, *args, **kwargs)
    return decorated_function


def create_first_admin(username, password):
    admin = User.query.filter_by(username="admin").first()
    if not admin:
        admin = User(
            username=username,
            password=generate_password_hash(password),
            role="admin"
        )
        db.session.add(admin)
        db.session.commit()
