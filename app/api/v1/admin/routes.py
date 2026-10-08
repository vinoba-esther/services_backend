from flask import Blueprint, request

from flask_jwt_extended import jwt_required

from app.core.decorators import admin_required

from app.core.responses import (
    error_response,
    success_response,
)

from app.schemas.user import (
    UserCreateRequest,
    UserUpdateRequest,
)

from app.services.admin_service import (
    AdminService,
)


admin_bp = Blueprint(
    "admin",
    __name__,
)


@admin_bp.get("/users")
@jwt_required()
@admin_required
def get_users():

    page = request.args.get(
        "page",
        default=1,
        type=int,
    )

    per_page = request.args.get(
        "per_page",
        default=20,
        type=int,
    )

    result = AdminService.get_users(
        page,
        per_page,
    )

    return success_response(
        data=result,
        message="Users fetched successfully",
    )


@admin_bp.get("/users/<int:user_id>")
@jwt_required()
@admin_required
def get_user(user_id):

    user = AdminService.get_user(
        user_id
    )

    if not user:

        return error_response(
            message="User not found",
            status_code=404,
        )

    return success_response(
        data=user,
        message="User fetched successfully",
    )


@admin_bp.post("/users")
@jwt_required()
@admin_required
def create_user():

    payload = UserCreateRequest.model_validate(
        request.get_json(
            silent=True
        ) or {}
    )

    try:

        user = AdminService.create_user(
            payload
        )

        return success_response(
            data=user,
            message="User created successfully",
            status_code=201,
        )

    except ValueError as error:

        return error_response(
            message=str(error),
            status_code=409,
        )


@admin_bp.patch("/users/<int:user_id>")
@jwt_required()
@admin_required
def update_user(user_id):

    payload = UserUpdateRequest.model_validate(
        request.get_json(
            silent=True
        ) or {}
    )

    try:

        user = AdminService.update_user(
            user_id,
            payload,
        )

        if not user:

            return error_response(
                message="User not found",
                status_code=404,
            )

        return success_response(
            data=user,
            message="User updated successfully",
        )

    except ValueError as error:

        return error_response(
            message=str(error),
            status_code=409,
        )


@admin_bp.delete("/users/<int:user_id>")
@jwt_required()
@admin_required
def delete_user(user_id):

    deleted = AdminService.delete_user(
        user_id
    )

    if not deleted:

        return error_response(
            message="User not found",
            status_code=404,
        )

    return success_response(
        message="User deleted successfully",
    )