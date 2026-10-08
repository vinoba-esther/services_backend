from flask import jsonify

from app.extensions import jwt


def register_jwt_handlers():

    @jwt.unauthorized_loader
    def unauthorized_callback(error):

        return jsonify({
            "success": False,
            "message": "Authentication token is required",
        }), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):

        return jsonify({
            "success": False,
            "message": "Invalid authentication token",
        }), 401

    @jwt.expired_token_loader
    def expired_token_callback(
        jwt_header,
        jwt_payload,
    ):

        return jsonify({
            "success": False,
            "message": "Authentication token has expired",
        }), 401