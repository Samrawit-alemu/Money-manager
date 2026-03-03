from fastapi import FastAPI
from app.api.v1.endpoints import user
from app.db.mongodb import get_database

app = FastAPI(title="Money Manager API")

app.include_router(user.router, prefix="/api/v1/users", tags=["users"])