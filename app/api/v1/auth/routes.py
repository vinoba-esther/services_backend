from flask import Blueprint, request

from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)

from app.core.responses import (
    error_response,
    success_response,
)

from app.extensions import limiter

from app.schemas.auth import LoginRequest

from app.services.auth_service import (
    AuthService,
)


auth_bp = Blueprint(
    "auth",
    __name__,
)


@auth_bp.post("/login")
@limiter.limit("5 per minute")
def login():

    payload = LoginRequest.model_validate(
        request.get_json(
            silent=True
        ) or {}
    )

    result = AuthService.login(
        str(payload.email),
        payload.password,
    )

    if not result:

        return error_response(
            message="Invalid email or password",
            status_code=401,
        )

    return success_response(
        data=result,
        message="Login successful",
    )


@auth_bp.get("/me")
@jwt_required()
def me():

    user_id = get_jwt_identity()

    return success_response(
        data={
            "user_id": int(user_id)
        },
        message="Current user",
    )