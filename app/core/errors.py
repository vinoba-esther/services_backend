from flask import jsonify
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import HTTPException

from app.extensions import db


def register_error_handlers(app):

    @app.errorhandler(ValidationError)
    def handle_validation_error(error):

        return jsonify({
            "success": False,
            "message": "Validation failed",
            "errors": error.errors(),
        }), 422

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(error):

        db.session.rollback()

        app.logger.exception(
            "Database integrity error"
        )

        return jsonify({
            "success": False,
            "message": "Database constraint error",
        }), 409

    @app.errorhandler(HTTPException)
    def handle_http_error(error):

        return jsonify({
            "success": False,
            "message": error.description,
        }), error.code

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):

        db.session.rollback()

        app.logger.exception(
            "Unhandled application error"
        )

        return jsonify({
            "success": False,
            "message": "Internal server error",
        }), 500