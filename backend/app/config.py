import os
from datetime import timedelta


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-for-local-development-only-32chars")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "dev-jwt-secret-key-for-local-development-only-32chars")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DB_USER = os.environ.get("DB_USER", "root")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "password")
    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_PORT = os.environ.get("DB_PORT", "3306")
    DB_NAME = os.environ.get("DB_NAME", "taskflow")

    DATABASE_URL = os.environ.get("DATABASE_URL") or os.environ.get("MYSQL_URL")

    if DATABASE_URL and DATABASE_URL.startswith("mysql://"):
        DATABASE_URL = DATABASE_URL.replace("mysql://", "mysql+pymysql://", 1)

    SQLALCHEMY_DATABASE_URI = DATABASE_URL or (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
