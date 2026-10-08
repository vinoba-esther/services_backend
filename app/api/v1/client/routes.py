from flask import Blueprint, request

from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)

from pydantic import BaseModel, Field

from app.core.responses import (
    error_response,
    success_response,
)

from app.services.client_service import (
    ClientService,
)


client_bp = Blueprint(
    "client",
    __name__,
)


class ProfileUpdateRequest(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=120,
    )


@client_bp.get("/profile")
@jwt_required()
def get_profile():

    user_id = int(
        get_jwt_identity()
    )

    profile = ClientService.get_profile(
        user_id
    )

    if not profile:

        return error_response(
            message="User not found",
            status_code=404,
        )

    return success_response(
        data=profile,
        message="Profile fetched successfully",
    )


@client_bp.patch("/profile")
@jwt_required()
def update_profile():

    user_id = int(
        get_jwt_identity()
    )

    payload = ProfileUpdateRequest.model_validate(
        request.get_json(
            silent=True
        ) or {}
    )

    profile = ClientService.update_profile(
        user_id,
        payload.name,
    )

    if not profile:

        return error_response(
            message="User not found",
            status_code=404,
        )

    return success_response(
        data=profile,
        message="Profile updated successfully",
    )