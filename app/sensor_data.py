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
    device_id = data.get('device_id')
    water_flow = data.get('water_flow')
    wind_speed = data.get('wind_speed')
    wind_orientation = data.get('wind_orientation')
    sun_insolation = data.get('sun_insolation')
    soil_temp = data.get('soil_temp')
    soil_hum = data.get('soil_hum')
    air_temp = data.get('air_temp')
    air_hum = data.get('air_hum')
    air_pressure = data.get('air_pressure')
    inside_air_temp = data.get('inside_air_temp')
    inside_air_hum = data.get('inside_air_hum')
    temp1 = data.get('temp1')
    temp2 = data.get('temp2')
    temp3 = data.get('temp3')
    soil_temp1 = data.get('soil_temp1')
    soil_hum1 = data.get('soil_hum1')
    soil_temp2 = data.get('soil_temp2')
    soil_hum2 = data.get('soil_hum2')

    if not device_id:
        return jsonify({"message": "Invalid data"}), 400

    new_data = SensorData(
        device_id=device_id,
        water_flow=water_flow,
        wind_speed=wind_speed,
        wind_orientation=wind_orientation,
        sun_insolation=sun_insolation,
        soil_temp=soil_temp,
        soil_hum=soil_hum,
        air_temp=air_temp,
        air_hum=air_hum,
        air_pressure=air_pressure,
        inside_air_temp=inside_air_temp,
        inside_air_hum=inside_air_hum,
        temp1=temp1,
        temp2=temp2,
        temp3=temp3,
        soil_temp1=soil_temp1,
        soil_hum1=soil_hum1,
        soil_temp2=soil_temp2,
        soil_hum2=soil_hum2,
    )
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
