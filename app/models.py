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
    temperature: Mapped[str]
    humidity: Mapped[str]
