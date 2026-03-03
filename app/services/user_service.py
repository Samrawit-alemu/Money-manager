from app.repositories.user_repo import UserRepository
from app.core.security  import hash_password, verify_password, create_access_token
from fastapi import HTTPException, status

class UserService:
    def __init__(self, db):
        self.repo = UserRepository(db)

    async def register_user(self, name:str, email: str, password: str):
        existing_user = await self.repo.get_by_email(email)

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
                )
        
        hashed_password = hash_password(password)

        user_data = {
            "name": name,
            "email": email,
            "password": hashed_password
        }
        return await self.repo.create_user(user_data)
    
    async def login_user(self, email: str, password: str):
        user = await self.repo.get_by_email(email)

        if not user:
            raise HTTPException(
                status_code=400,
                detail="Invalid credentials"
            )

        if not verify_password(password, user["password"]):
            raise HTTPException(
                status_code=400,
                detail="Invalid credentials"
            )

        access_token = create_access_token(
            data={"sub": str(user["_id"])}
        )

        return access_token
