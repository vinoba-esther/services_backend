from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt


def admin_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        claims = get_jwt()

        if claims.get("role") != "admin":

            return jsonify({
                "success": False,
                "message": "Admin access required",
            }), 403

        return func(*args, **kwargs)

    return wrapper