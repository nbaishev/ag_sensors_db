from flask import (
    Blueprint, jsonify, request
)
from flask_jwt_extended import jwt_required

from app.database import db
from app.models import Controller, SensorData
from app.utils import require_api_key, admin_required

bp = Blueprint('data', __name__, url_prefix='/data')


@bp.route('/add', methods=('POST',))
@require_api_key
def add_data(controller):
    data = request.get_json()
    temperature = data.get('temperature')
    humidity = data.get('humidity')

    if not temperature or not humidity:
        return jsonify({"message": "Invalid data"}), 400

    new_data = SensorData(temperature=temperature, humidity=humidity)
    db.session.add(new_data)
    db.session.commit()

    return jsonify({"message": "Data added successfully"}), 201


@bp.route('/get', methods=('GET',))
@jwt_required()
def get_data():
    data = SensorData.query.all()
    result = [{"timestamp": d.created, "temperature": d.temperature, "humidity": d.humidity} for d in data]
    return jsonify(result)


@bp.route('/register_controller', methods=['POST'])
@jwt_required()
@admin_required
def register_controller():
    data = request.get_json()
    sensor_name = data.get("sensor_name")

    if not sensor_name:
        return jsonify({"error": "Sensor name is required"}), 400

    new_sensor = Controller(sensor_name=sensor_name)
    db.session.add(new_sensor)
    db.session.commit()

    return jsonify({"message": "Sensor registered", "api_key": new_sensor.api_key}), 201


@bp.route('/plot', methods=['POST'])
def plot():
    data = request.get_json()
    sensor_name = data.get("sensor_name")

    if not sensor_name:
        return jsonify({"error": "Sensor name is required"}), 400

    new_sensor = Controller(sensor_name=sensor_name)
    db.session.add(new_sensor)
    db.session.commit()

    return jsonify({"message": "Sensor registered", "api_key": new_sensor.api_key}), 201
