from fastapi import FastAPI
from app.db.mongodb import get_database

app = FastAPI(title="Money Manager API")

@app.on_event("startup")
async def startup_db_client():
    db = get_database()
    print("Connected to MongoDB:", db.name)


@app.get("/")
async def root():
    return {"message": "Money Manager API is running"}