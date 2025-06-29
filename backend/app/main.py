from fastapi import FastAPI
from app.api.routes import all_routes
from app.db.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Register all routers dynamically
for router, prefix, tag in all_routes:
    app.include_router(router, prefix=prefix, tags=[tag])
