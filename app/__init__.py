import os

from flask import Flask
from flask_jwt_extended import JWTManager

from app.utils import create_first_admin


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    jwt = JWTManager(app)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'project.db'),
    )

    if test_config is None:
        from .config import DevelopmentConfig
        app.config.from_object(DevelopmentConfig())
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from app.database import db
    db.init_app(app)

    from app.models import SensorData, User
    with app.app_context():
        db.create_all()
        create_first_admin(
            username=app.config['ADMIN_USERNAME'],
            password=app.config['ADMIN_PASSWORD']
        )

    from . import sensor_data
    app.register_blueprint(sensor_data.bp)
    from . import auth
    app.register_blueprint(auth.bp)

    return app
