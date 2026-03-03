from datetime import datetime
from bson import ObjectId

class UserRepository:
    def __init__(self, db):
        self.collection = db["users"]
    
    async def get_by_email(self, email: str):
        return await self.collection.find_one({"email": email})    

    async def create_user(self, user_data):
        user_data["created_at"] = datetime.utcnow()
        result = await self.collection.insert_one(user_data)
        return await self.collection.find_one({"_id": result.inserted_id})

