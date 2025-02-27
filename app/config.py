import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    """Base config, uses staging database server."""
    TESTING = False
    DB_SERVER = '192.168.1.56'


class ProductionConfig(Config):
    """Uses production database server."""
    DB_SERVER = '192.168.19.32'


class DevelopmentConfig(Config):
    DB_SERVER = 'localhost'
    SECRET_KEY = os.getenv("SECRET_KEY", "secret")
    DB_NAME = os.getenv("DB_NAME", "postgres")
    DB_USER = os.getenv("POSTGRES_USER", "postgres")
    DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
    DB_HOST = os.getenv("DB_HOST", "db")
    DB_PORT = os.getenv("DB_PORT", "5432")
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin")
    JWT_SECRET_KEY = os.getenv("ADMIN_PASSWORD", "secret")


class TestingConfig(Config):
    SECRET_KEY = os.getenv("SECRET_KEY", "secret")
    DB_SERVER = 'localhost'
    DB_NAME = os.getenv("DB_NAME", "postgres")
    DB_USER = os.getenv("POSTGRES_USER", "postgres")
    DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///project.db'
