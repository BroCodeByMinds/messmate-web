from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse, JSONResponse
from app.config.loader import ConfigLoader
from app.utils.oauth_config import oauth
from app.services.user_service import UserService
from app.db.database import get_db
from sqlalchemy.orm import Session
import os

router = APIRouter()

google_cfg = ConfigLoader().get_google_oauth_config()


@router.get("/auth/google")
async def login_with_google(request: Request):
    role = request.query_params.get("role", "student")  # default to student
    request.session["role"] = role  # Store in session for callback
    redirect_uri = google_cfg["redirect_uri"]
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/auth/google/callback")
async def google_auth_callback(request: Request, db: Session = Depends(get_db)):
    token = await oauth.google.authorize_access_token(request)
    user_info = await oauth.google.parse_id_token(request, token)

    email = user_info.get("email")
    name = user_info.get("name")
    role = request.session.get("role", "student")

    # 🛑 Don't allow admin role from session!
    if role == "admin":
        # Only allow pre-approved admin emails
        allowed_admins = ["admin@yourdomain.com"]
        if email not in allowed_admins:
            role = "student"  # downgrade

    # Login/Register logic
    service = UserService(db)
    return service.login_or_register_oauth_user(email=email, name=name, role=role)

