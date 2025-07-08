from sqlalchemy.orm import Session
from app.models.user_orm import UserORM

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str) -> UserORM | None:
        return self.db.query(UserORM).filter(UserORM.email == email).first()

    def create_user(self, user: UserORM) -> UserORM:
        self.db.add(user)
        self.db.flush()  # Ensures ID is generated
        self.db.refresh(user)
        return user

