from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class TransactionType(str, Enum):
    income = "income"
    expense = "expense"


class TransactionCreate(BaseModel):
    amount: float = Field(..., gt=0)
    type: TransactionType
    category: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None


class TransactionResponse(BaseModel):
    id: str
    amount: float
    type: TransactionType
    category: str
    description: Optional[str]
    created_at: datetime