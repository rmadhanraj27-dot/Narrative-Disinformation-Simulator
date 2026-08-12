from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.database.mongodb import database
from app.models.user import create_user_document, user_response
from app.schemas.user import UserRegister
from app.utils.auth_dependencies import (
    get_current_user,
    get_optional_current_user
)
from app.utils.security import (
    create_access_token,
    hash_password,
    verify_password
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# ============================================================
# REGISTER
# ============================================================

@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED
)
async def register_user(user: UserRegister):

    # Check if email already exists
    existing_user = await database.users.find_one(
        {
            "email": user.email.lower().strip()
        }
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered"
        )

    # Hash the password
    password_hash = hash_password(
        user.password
    )

    # Create user document
    user_document = create_user_document(
        name=user.name,
        email=user.email,
        password_hash=password_hash
    )

    # Save user to MongoDB
    result = await database.users.insert_one(
        user_document
    )

    # Get newly created user
    created_user = await database.users.find_one(
        {
            "_id": result.inserted_id
        }
    )

    return {
        "message": "User registered successfully",
        "user": user_response(created_user)
    }


# ============================================================
# LOGIN
# ============================================================

@router.post("/login")
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends()
):

    # Get email from username field
    email = form_data.username.lower().strip()

    # Find user
    user = await database.users.find_one(
        {
            "email": email
        }
    )

    # User does not exist
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    # Verify password
    password_valid = verify_password(
        form_data.password,
        user["password_hash"]
    )

    # Password is incorrect
    if not password_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    # Create JWT token
    access_token = create_access_token(
        str(user["_id"])
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_response(user)
    }


# ============================================================
# GET CURRENT USER
# ============================================================

@router.get("/me")
async def get_me(
    current_user: dict = Depends(
        get_current_user
    )
):

    return {
        "user": user_response(
            current_user
        )
    }


# ============================================================
# OPTIONAL AUTHENTICATION / SESSION
# ============================================================

@router.get("/session")
async def get_session(
    current_user: dict | None = Depends(
        get_optional_current_user
    )
):

    # Guest user
    if current_user is None:

        return {
            "authenticated": False,
            "user": None,
            "message": (
                "You are using the application "
                "as a guest."
            )
        }

    # Logged-in user
    return {
        "authenticated": True,
        "user": user_response(
            current_user
        ),
        "message": "You are logged in."
    }

