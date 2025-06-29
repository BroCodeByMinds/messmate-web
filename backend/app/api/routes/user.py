from fastapi import APIRouter, Depends
from app.core.deps import get_current_user
from app.schemas.user import UserResponse

router = APIRouter()

@router.get("/user_profile", response_model=UserResponse)
def get_profile(current_user = Depends(get_current_user)):
    return current_user
