from typing import Optional

from bson import ObjectId
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.config.settings import settings
from app.database.mongodb import database


# Required authentication
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


# ============================================================
# REQUIRED AUTHENTICATION
# ============================================================

async def get_current_user(
    token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer"
        }
    )

    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    if not ObjectId.is_valid(user_id):
        raise credentials_exception

    user = await database.users.find_one(
        {
            "_id": ObjectId(user_id)
        }
    )

    if user is None:
        raise credentials_exception

    return user


# ============================================================
# OPTIONAL AUTHENTICATION
# ============================================================

optional_oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
    auto_error=False
)


async def get_optional_current_user(
    token: Optional[str] = Depends(
        optional_oauth2_scheme
    )
):

    # No token = Guest user
    if not token:
        return None

    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm]
        )

        user_id = payload.get("sub")

        if not user_id:
            return None

        if not ObjectId.is_valid(user_id):
            return None

        user = await database.users.find_one(
            {
                "_id": ObjectId(user_id)
            }
        )

        return user

    except JWTError:
        return None