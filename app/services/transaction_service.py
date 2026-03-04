from bson import ObjectId
from app.repositories.transaction_repo import TransactionRepository


class TransactionService:
    def __init__(self, db):
        self.repo = TransactionRepository(db)

    async def create_transaction(self, user_id: str, data):
        transaction_dict = data.dict()
        transaction_dict["user_id"] = ObjectId(user_id)

        transaction = await self.repo.create(transaction_dict)
        return transaction

    async def get_user_transactions(self, user_id: str):
        return await self.repo.get_by_user(user_id)
    

    async def calculate_balance(self, user_id: str):
        return await self.repo.get_balance_aggregation(user_id)