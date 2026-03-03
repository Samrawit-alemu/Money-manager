import re
from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")

        if len(value) > 72:
            raise ValueError("Password must not exceed 72 characters")

        if not re.search(r"[A-Za-z]", value):
            raise ValueError("Password must contain at least one letter")

        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one number")

        return value

class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    created_at: datetime
