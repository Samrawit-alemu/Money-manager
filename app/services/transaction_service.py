from bson import ObjectId
from fastapi import HTTPException
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
    

    async def calculate_balance(self, user_id: str, month: int | None = None, year: int | None = None):
        return await self.repo.get_balance_aggregation(user_id, month, year) # type: ignore
    
    async def update_transaction(self, transaction_id: str, user_id: str, update_data: dict):
        if not ObjectId.is_valid(transaction_id):
            raise HTTPException(status_code=400, detail="Invalid transaction ID")
        
        updated_item = await self.repo.update_transaction(transaction_id, user_id, update_data)

        if not updated_item:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        return updated_item
    
    async def delete_transaction(self, transaction_id: str, user_id: str):
        if not ObjectId.is_valid(transaction_id):
            raise HTTPException(status_code=400, detail="Invalid transaction ID")
        
        success = await self.repo.delete_transaction(transaction_id, user_id)

        if not success:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        return {"message": "Transaction deleted successfully"}