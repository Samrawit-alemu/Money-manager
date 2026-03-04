import token

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from bson import ObjectId

from app.core.config import settings
from app.db.mongodb import get_database

# extracts token from header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/users/login") 

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db=Depends(get_database)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    try: 
        # decode token
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )

# get user_d from token 
        user_id: str = payload.get("sub") # type: ignore

        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    # fetch user from database using user_id
    user = await db.users.find_one({"_id": ObjectId(user_id)})

    if user is None:
        raise credentials_exception
    
    # attach user to route
    return user