from app.extensions import db

from app.repositories.user_repository import (
    UserRepository,
)


class ClientService:

    @staticmethod
    def get_profile(user_id):

        user = UserRepository.get_by_id(
            user_id
        )

        if not user:
            return None

        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "is_active": user.is_active,
        }

    @staticmethod
    def update_profile(
        user_id,
        name,
    ):

        user = UserRepository.get_by_id(
            user_id
        )

        if not user:
            return None

        user.name = name

        db.session.commit()

        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
        }