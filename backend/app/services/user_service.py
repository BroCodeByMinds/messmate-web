from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import timedelta
from app.core.security import get_password_hash, verify_password, create_access_token
from app.models.user_orm import UserORM
from app.repositories.user_repository import UserRepository

class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def register_user(self, name: str, email: str, password: str, phone: str) -> UserORM:
        if self.repo.get_user_by_email(email):
            raise HTTPException(status_code=400, detail="Email already registered")

        hashed_pw = get_password_hash(password)
        user_data = {
            "name": name,
            "email": email,
            "phone": phone,
            "hashed_password": hashed_pw
        }
        return self.repo.create_user(user_data)

    def login_user(self, email: str, password: str) -> str:
        user = self.repo.get_user_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        return create_access_token(
            data={"sub": str(user.id)},
            expires_delta=timedelta(minutes=30)
        )
