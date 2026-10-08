from flask_jwt_extended import create_access_token

from app.repositories.user_repository import (
    UserRepository,
)


class AuthService:

    @staticmethod
    def login(email, password):

        user = UserRepository.get_by_email(
            email
        )

        if not user:
            return None

        if not user.is_active:
            return None

        if not user.check_password(password):
            return None

        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={
                "role": user.role,
            },
        )

        return {
            "access_token": access_token,
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role,
            },
        }