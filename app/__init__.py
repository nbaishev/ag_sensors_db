import os

from flask import Blueprint, Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from app.utils import create_first_admin


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    jwt = JWTManager(app)

    if test_config is None:
        from .config import DevelopmentConfig
        app.config.from_object(DevelopmentConfig())
    else:
        app.config.from_mapping(test_config)

    CORS(app, resources={
        r"/api/*": {
            "origins": app.config.get('TRUSTED_DOMAINS').split(",")
        }
    })

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from app.database import db
    db.init_app(app)

    from app.models import SensorData, User
    with app.app_context():
        db.create_all()
        create_first_admin(
            username=app.config['ADMIN_USERNAME'],
            password=app.config['ADMIN_PASSWORD']
        )

    api = Blueprint('api', __name__, url_prefix='/api')
    from . import sensor_data
    api.register_blueprint(sensor_data.bp)
    from . import auth
    api.register_blueprint(auth.bp)

    app.register_blueprint(api)

    return app
