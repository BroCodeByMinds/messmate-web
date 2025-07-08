from sqlalchemy.orm import Session
from app.db.database import get_db
from fastapi import APIRouter, Depends
from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserResponse
from fastapi.security import OAuth2PasswordRequestForm
from app.utils.response_builder import ResponseBuilder


router = APIRouter()

def get_response_builder() -> ResponseBuilder:
    return ResponseBuilder()


@router.post("/register", response_model=UserResponse)
def register(
    user: UserCreate,
    db: Session = Depends(get_db),
    resp_builder: ResponseBuilder = Depends(get_response_builder),
):
    service = UserService(db, resp_builder)
    return service.register_user(user)

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    service = UserService(db)
    token = service.login_user(
        email=form_data.username,
        password=form_data.password
    )
    return {"access_token": token, "token_type": "bearer"}
