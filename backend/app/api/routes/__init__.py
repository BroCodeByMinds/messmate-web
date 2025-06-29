from .auth import router as auth_router
from .user import router as user_router


all_routes = [
    (auth_router, "/api", "Auth"),
    (user_router, "/api", "User"),
]
