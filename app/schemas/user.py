from typing import Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
)


class UserCreateRequest(BaseModel):

    model_config = ConfigDict(
        extra="forbid"
    )

    name: str = Field(
        min_length=2,
        max_length=120,
    )

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=100,
    )

    role: Literal[
        "admin",
        "client",
    ] = "client"


class UserUpdateRequest(BaseModel):

    model_config = ConfigDict(
        extra="forbid"
    )

    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=120,
    )

    email: EmailStr | None = None

    role: Literal[
        "admin",
        "client",
    ] | None = None

    is_active: bool | None = None