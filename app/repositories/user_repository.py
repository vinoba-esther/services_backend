from app.extensions import db
from app.models.user import User


class UserRepository:

    @staticmethod
    def get_by_id(user_id):

        return db.session.scalar(
            db.select(User).where(
                User.id == user_id
            )
        )

    @staticmethod
    def get_by_email(email):

        return db.session.scalar(
            db.select(User).where(
                User.email == email
            )
        )

    @staticmethod
    def get_paginated(
        page=1,
        per_page=20,
    ):

        statement = (
            db.select(User)
            .order_by(User.id.desc())
        )

        return db.paginate(
            statement,
            page=page,
            per_page=per_page,
            max_per_page=100,
            error_out=False,
        )

    @staticmethod
    def create(user):

        db.session.add(user)

    @staticmethod
    def delete(user):

        db.session.delete(user)