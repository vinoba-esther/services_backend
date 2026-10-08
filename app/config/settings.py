import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()


class BaseConfig:

    SECRET_KEY = os.getenv("SECRET_KEY")

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        minutes=15
    )

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 280,
    }

    CORS_ORIGINS = [
        origin.strip()
        for origin in os.getenv(
            "CORS_ORIGINS",
            ""
        ).split(",")
        if origin.strip()
    ]


class DevelopmentConfig(BaseConfig):

    DEBUG = True
    TESTING = False


class TestingConfig(BaseConfig):

    DEBUG = False
    TESTING = True

    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///:memory:"
    )


class ProductionConfig(BaseConfig):

    DEBUG = False
    TESTING = False