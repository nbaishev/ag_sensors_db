import datetime
import uuid

from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import db


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    role: Mapped[str] = mapped_column(default="user")


class Controller(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sensor_name: Mapped[str] = mapped_column(unique=True)
    api_key: Mapped[str] = mapped_column(unique=True, nullable=False, default=lambda: str(uuid.uuid4()))


class SensorData(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created: Mapped[datetime.datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP"))
    device_id: Mapped[int] = mapped_column(unique=True)
    water_flow: Mapped[float]
    wind_speed: Mapped[float]
    wind_orientation: Mapped[float]
    sun_insolation: Mapped[float]
    soil_temp: Mapped[float]
    soil_hum: Mapped[float]
    air_temp: Mapped[float]
    air_hum: Mapped[float]
    air_pressure: Mapped[float]
    inside_air_temp: Mapped[float]
    inside_air_hum: Mapped[float]
    temp1: Mapped[float]
    temp2: Mapped[float]
    temp3: Mapped[float]
    soil_temp1: Mapped[float]
    soil_hum1: Mapped[float]
    soil_temp2: Mapped[float]
    soil_hum2: Mapped[float]
