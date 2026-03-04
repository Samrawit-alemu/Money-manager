from datetime import datetime
from bson import ObjectId


class TransactionRepository:
    def __init__(self, db):
        self.collection = db.transactions

    async def create(self, transaction_data: dict):
        transaction_data["created_at"] = datetime.utcnow()
        result = await self.collection.insert_one(transaction_data)
        transaction_data["_id"] = result.inserted_id
        return transaction_data

    async def get_by_user(self, user_id: str):
        transactions = []
        cursor = self.collection.find({"user_id": ObjectId(user_id)})
        async for doc in cursor:
            transactions.append(doc)
        return transactions