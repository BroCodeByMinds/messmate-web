from datetime import timedelta
from fastapi import HTTPException
from app.constants import messages
from sqlalchemy.orm import Session
from app.models.user_orm import UserORM
from sqlalchemy.exc import SQLAlchemyError
from fastapi.responses import JSONResponse
from app.schemas.user import UserCreate, UserResponse
from app.utils.response_builder import ResponseBuilder
from app.repositories.user_repository import UserRepository
from app.core.security import get_password_hash, verify_password, create_access_token


class UserService:
    def __init__(self, db: Session, resp_builder: ResponseBuilder):
        self.repo = UserRepository(db)
        self.resp_builder = resp_builder

    def register_user(self, user_create: UserCreate) -> JSONResponse:
        """
        Registers a new user in the system.

        - Ensures email uniqueness.
        - Hashes the password securely.
        - Stores user data in the database within a transactional scope.

        Returns:
            JSONResponse: A structured success or error response with appropriate HTTP status code.
        """
        try:
            with self.repo.db.begin():  # Atomic transaction
                if self.repo.get_user_by_email(user_create.email):
                    return self.resp_builder.build_conflict_response(
                        messages.EMAIL_ALREADY_EXISTS
                    )

                hashed_pw = get_password_hash(user_create.password)
                user_data = user_create.model_dump(exclude={"password"})
                user = UserORM(**user_data, hashed_password=hashed_pw)

                created_user = self.repo.create_user(user)

            return self.resp_builder.build_created_response(
                messages.USER_REGISTERED_SUCCESSFULLY,
                UserResponse(
                    user_id=created_user.id,
                    email=created_user.email
                ).model_dump()
            )

        except SQLAlchemyError as db_error:
            self.repo.db.rollback()
            return self.resp_builder.build_server_error_response(
                messages.USER_REGISTRATION_FAILED,
                {"db_error": str(db_error)}
            )

        except Exception as exc:
            self.repo.db.rollback()
            return self.resp_builder.build_server_error_response(
                messages.USER_REGISTRATION_FAILED,
                {"error": str(exc)}
            )
    

    def login_user(self, email: str, password: str) -> str:
        user = self.repo.get_user_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        return create_access_token(
            data={"sub": str(user.id)},
            expires_delta=timedelta(minutes=30)
        )
