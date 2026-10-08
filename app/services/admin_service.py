from app.extensions import db
from app.models.user import User
from app.repositories.user_repository import (
    UserRepository,
)


class AdminService:

    @staticmethod
    def get_users(page=1, per_page=20):

        pagination = (
            UserRepository.get_paginated(
                page=page,
                per_page=per_page,
            )
        )

        users = [
            AdminService._serialize_user(user)
            for user in pagination.items
        ]

        return {
            "items": users,
            "pagination": {
                "page": pagination.page,
                "per_page": pagination.per_page,
                "pages": pagination.pages,
                "total": pagination.total,
                "has_next": pagination.has_next,
                "has_prev": pagination.has_prev,
            },
        }

    @staticmethod
    def get_user(user_id):

        user = UserRepository.get_by_id(
            user_id
        )

        if not user:
            return None

        return AdminService._serialize_user(
            user
        )

    @staticmethod
    def create_user(data):

        existing_user = (
            UserRepository.get_by_email(
                str(data.email)
            )
        )

        if existing_user:

            raise ValueError(
                "Email already exists"
            )

        user = User(
            name=data.name,
            email=str(data.email),
            role=data.role,
            is_active=True,
        )

        user.set_password(
            data.password
        )

        UserRepository.create(user)

        db.session.commit()

        return AdminService._serialize_user(
            user
        )

    @staticmethod
    def update_user(user_id, data):

        user = UserRepository.get_by_id(
            user_id
        )

        if not user:
            return None

        if data.name is not None:
            user.name = data.name

        if data.email is not None:

            existing = (
                UserRepository.get_by_email(
                    str(data.email)
                )
            )

            if existing and existing.id != user.id:

                raise ValueError(
                    "Email already exists"
                )

            user.email = str(data.email)

        if data.role is not None:
            user.role = data.role

        if data.is_active is not None:
            user.is_active = data.is_active

        db.session.commit()

        return AdminService._serialize_user(
            user
        )

    @staticmethod
    def delete_user(user_id):

        user = UserRepository.get_by_id(
            user_id
        )

        if not user:
            return False

        UserRepository.delete(user)

        db.session.commit()

        return True

    @staticmethod
    def _serialize_user(user):

        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "is_active": user.is_active,
            "created_at": user.created_at.isoformat(),
            "updated_at": user.updated_at.isoformat(),
        }