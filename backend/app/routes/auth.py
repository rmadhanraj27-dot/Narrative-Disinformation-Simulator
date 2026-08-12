from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.database.mongodb import database
from app.models.user import create_user_document, user_response
from app.schemas.user import UserRegister
from app.utils.security import (
    create_access_token,
    hash_password,
    verify_password
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED
)
async def register_user(user: UserRegister):

    existing_user = await database.users.find_one(
        {"email": user.email.lower().strip()}
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered"
        )

    password_hash = hash_password(user.password)

    user_document = create_user_document(
        name=user.name,
        email=user.email,
        password_hash=password_hash
    )

    result = await database.users.insert_one(
        user_document
    )

    created_user = await database.users.find_one(
        {"_id": result.inserted_id}
    )

    return {
        "message": "User registered successfully",
        "user": user_response(created_user)
    }


@router.post("/login")
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends()
):

    email = form_data.username.lower().strip()

    user = await database.users.find_one(
        {"email": email}
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    password_valid = verify_password(
        form_data.password,
        user["password_hash"]
    )

    if not password_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        str(user["_id"])
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_response(user)
    }