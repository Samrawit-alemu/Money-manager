from fastapi import APIRouter, Depends
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import UserService
from app.db.mongodb import get_database
from bson import ObjectId

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate, db=Depends(get_database)):
    service = UserService(db)
    new_user = await service.register_user(
        user.name,
        user.email,
        user.password
    )

    return UserResponse(
        id=str(new_user["_id"]),
        name=new_user["name"],
        email=new_user["email"],
        created_at=new_user["created_at"]
    )