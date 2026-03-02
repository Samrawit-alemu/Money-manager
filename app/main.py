from fastapi import FastAPI

app = FastAPI(title="Money Manager API")

@app.get("/")
async def root():
    return {"message": "Money Manager API is running"}