from fastapi import APIRouter, Depends
from app.schemas.transaction import TransactionCreate, TransactionResponse
from app.services.transaction_service import TransactionService
from app.core.dependencies import get_current_user
from app.db.mongodb import get_database

router = APIRouter()


@router.post("/", response_model=TransactionResponse)
async def create_transaction(
    transaction: TransactionCreate,
    current_user=Depends(get_current_user),
    db=Depends(get_database)
):
    service = TransactionService(db)

    new_transaction = await service.create_transaction(
        user_id=str(current_user["_id"]),
        data=transaction
    )

    return {
        "id": str(new_transaction["_id"]),
        "amount": new_transaction["amount"],
        "type": new_transaction["type"],
        "category": new_transaction["category"],
        "description": new_transaction.get("description"),
        "created_at": new_transaction["created_at"]
    }


@router.get("/", response_model=list[TransactionResponse])
async def get_my_transactions(
    current_user=Depends(get_current_user),
    db=Depends(get_database)
):
    service = TransactionService(db)

    transactions = await service.get_user_transactions(
        user_id=str(current_user["_id"])
    )

    return [
        {
            "id": str(t["_id"]),
            "amount": t["amount"],
            "type": t["type"],
            "category": t["category"],
            "description": t.get("description"),
            "created_at": t["created_at"]
        }
        for t in transactions
    ]

@router.get("/summary")
async def get_summary(
    current_user=Depends(get_current_user),
    db=Depends(get_database)
):
    service = TransactionService(db)

    return await service.calculate_balance(
        user_id=str(current_user["_id"])
    )