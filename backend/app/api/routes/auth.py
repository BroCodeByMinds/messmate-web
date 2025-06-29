from sqlalchemy.orm import Session
from app.db.database import get_db
from fastapi import APIRouter, Depends
from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserResponse
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.register_user(
        name=user.name,
        email=user.email,
        password=user.password,
        phone=user.phone
    )

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    service = UserService(db)
    token = service.login_user(
        email=form_data.username,
        password=form_data.password
    )
    return {"access_token": token, "token_type": "bearer"}
