from datetime import datetime

from fastapi import APIRouter, Depends, Query, HTTPException
from app.schemas.transaction import TransactionCreate, TransactionResponse, TransactionUpdate
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
            "created_at": t.get("created_at", datetime.utcnow())
        }
        for t in transactions
    ]

@router.get("/summary")
async def get_summary(
    month: int | None = Query(None, ge=1, le=12),
    year: int | None = Query(None, ge=2000, le=2100),
    current_user=Depends(get_current_user),
    db=Depends(get_database)
):
    service = TransactionService(db)

    summary = await service.calculate_balance(
        user_id=str(current_user["_id"]),
        month=month, # type: ignore
        year=year # type: ignore
    )

    return summary

@router.patch("/{transaction_id}", response_model=TransactionResponse)
async def update_transaction(
    transaction_id: str,
    update_data: TransactionUpdate,
    current_user=Depends(get_current_user),
    db=Depends(get_database)
):
    service = TransactionService(db)

    clean_data = update_data.model_dump(exclude_unset=True)

    if not clean_data:
        raise HTTPException(status_code=400, detail="No update data provided") # type: ignore

    updated_item = await service.update_transaction(
        transaction_id=transaction_id,
        user_id=str(current_user["_id"]), 
        update_data=clean_data
    )
    

    return {
        "id": str(updated_item["_id"]),
        "amount": updated_item["amount"],
        "type": updated_item["type"],
        "category": updated_item["category"],
        "description": updated_item.get("description"),
        "created_at": updated_item["created_at"]
    }

@router.delete("/{transaction_id}")
async def delete_transaction(
    transaction_id: str,
    current_user=Depends(get_current_user),
    db=Depends(get_database)
):
    service = TransactionService(db)

    return await service.delete_transaction(transaction_id=transaction_id, user_id=str(current_user["_id"]))