from app import create_app

from app.extensions import db

from app.models.user import User


app = create_app("development")


with app.app_context():

    email = "admin@example.com"

    existing = db.session.scalar(
        db.select(User).where(
            User.email == email
        )
    )

    if existing:

        print("Admin already exists")

    else:

        admin = User(
            name="System Admin",
            email=email,
            role="admin",
            is_active=True,
        )

        admin.set_password(
            "Admin@12345"
        )

        db.session.add(admin)

        db.session.commit()

        print(
            "Admin created successfully"
        )