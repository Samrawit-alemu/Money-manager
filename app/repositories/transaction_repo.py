from bson import ObjectId
from pymongo import ReturnDocument


class TransactionRepository:
    def __init__(self, db):
        self.collection = db["transactions"]

    async def create(self, transaction_data: dict):
        """
        Create a new transaction
        """
        result = await self.collection.insert_one(transaction_data)
        transaction_data["_id"] = result.inserted_id
        return transaction_data

    async def get_by_user(self, user_id: str):
        """
        Get all transactions for a specific user
        """
        cursor = self.collection.find({"user_id": ObjectId(user_id)})

        transactions = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            doc["user_id"] = str(doc["user_id"])
            transactions.append(doc)

        return transactions

    async def get_balance_aggregation(self, user_id: str, month: int | None = None, year: int | None = None):
        """
        Calculate total income, expense and balance using MongoDB aggregation
        """

        match_stage = {"user_id": ObjectId(user_id)}

        pipeline: list[dict] = [
            {"$match": match_stage}
        ]

        # Optional date filtering
        if month or year:
            expr_conditions = []

            if month:
                expr_conditions.append({"$eq": [{"$month": "$created_at"}, month]})

            if year:
                expr_conditions.append({"$eq": [{"$year": "$created_at"}, year]})

            pipeline.append({
                "$match": {
                    "$expr": {
                        "$and": expr_conditions
                    }
                }
            })

        # Group transactions by type (income / expense)
        pipeline.append({
            "$group": {
                "_id": "$type", # type: ignore
                "total": {"$sum": "$amount"}
            }
        })

        cursor = self.collection.aggregate(pipeline)

        result = {
            "income": 0,
            "expense": 0
        }

        async for doc in cursor:
            result[doc["_id"]] = doc["total"]

        result["balance"] = result["income"] - result["expense"]

        return result

    async def update_transaction(self, transaction_id: str, user_id: str, update_data: dict):
        """
        Update a transaction by its ID
        """
        result = await self.collection.find_one_and_update(
            {"_id": ObjectId(transaction_id), "user_id": ObjectId(user_id)},
            {"$set": update_data},
            return_document=ReturnDocument.AFTER
        )

        return result
    
    async def delete_transaction(self, transaction_id: str, user_id: str) -> bool:
        """
        Delete a transaction by its ID
        """
        result = await self.collection.delete_one({"_id": ObjectId(transaction_id), "user_id": ObjectId(user_id)})

        return result.deleted_count > 0
        
    