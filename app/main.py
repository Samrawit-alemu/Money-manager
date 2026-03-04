from fastapi import FastAPI
from app.api.v1.endpoints import user, transaction
from app.api.v1.router import api_router
from app.db.mongodb import get_database

app = FastAPI(title="Money Manager API")

app.include_router(api_router, prefix="/api/v1")