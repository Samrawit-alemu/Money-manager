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
    
    async def get_balance_aggregation(self, user_id: str):
        pipeline = [
            {"$match": {"user_id": ObjectId(user_id)}},
            {
                "$group": {
                    "_id": "$type",
                    "total": {"$sum": "$amount"}
                }
            }
        ]
        cursor = self.collection.aggregate(pipeline)
        result = {"income": 0, "expense": 0}

        async for doc in cursor:
            result[doc["_id"]] = doc["total"]

        result["balance"] = result["income"] - result["expense"]
        return result