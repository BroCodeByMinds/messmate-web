from fastapi import FastAPI
from app.api.routes import all_routes
from app.config.loader import ConfigLoader
from app.db.database import Base, engine
from starlette.middleware.sessions import SessionMiddleware


google_cfg = ConfigLoader().get_google_oauth_config()
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key=google_cfg['secret_key'])


# Register all routers dynamically
for router, prefix, tag in all_routes:
    app.include_router(router, prefix=prefix, tags=[tag])
