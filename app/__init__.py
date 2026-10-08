import os

from flask import Flask

from app.config.settings import (
    DevelopmentConfig,
    TestingConfig,
    ProductionConfig,
)

from app.extensions import (
    db,
    migrate,
    jwt,
    limiter,
    cors,
)

from app.core.errors import register_error_handlers
from app.core.security import register_jwt_handlers


def create_app(config_name=None):

    app = Flask(__name__)

    config_name = config_name or os.getenv(
        "FLASK_ENV",
        "development",
    )

    configs = {
        "development": DevelopmentConfig,
        "testing": TestingConfig,
        "production": ProductionConfig,
    }

    config_class = configs.get(
        config_name,
        DevelopmentConfig,
    )

    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    limiter.init_app(app)

    cors.init_app(
        app,
        resources={
            r"/api/*": {
                "origins": app.config["CORS_ORIGINS"]
            }
        },
    )

    # Import models
    from app.models.user import User

    # Register error handlers
    register_error_handlers(app)

    # Register JWT handlers
    register_jwt_handlers()

    # Register API Blueprints
    from app.api.v1.auth.routes import auth_bp
    from app.api.v1.admin.routes import admin_bp
    from app.api.v1.client.routes import client_bp

    app.register_blueprint(
        auth_bp,
        url_prefix="/api/v1/auth",
    )

    app.register_blueprint(
        admin_bp,
        url_prefix="/api/v1/admin",
    )

    app.register_blueprint(
        client_bp,
        url_prefix="/api/v1/client",
    )

    # Health check
    @app.get("/health")
    def health_check():

        return {
            "success": True,
            "message": "API is running",
        }, 200

    return app