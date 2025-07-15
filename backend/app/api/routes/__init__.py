from .auth import router as auth_router
from .oauth import router as oauth_router

all_routes = [
    (auth_router, "/api", "Auth"),
    (oauth_router, "/api", "User"),
]
