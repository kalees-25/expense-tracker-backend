# routers/auth.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from core.database.connection import get_db

from schemas.auth import (
    UserCreate,
    UserLogin,
    UserResponse,
    TokenResponse
)

from services.auth_services import (
    register_user,
    login_user
)

from core.security import get_current_user

from models.users import User


from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# ---------------------------------------------------
# REGISTER USER
# ---------------------------------------------------

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):

    """
    Register a new user
    """

    user = register_user(
        db=db,
        user_data=user_data
    )

    return user


# ---------------------------------------------------
# LOGIN USER
# ---------------------------------------------------

@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK
)
def login(
    # user_data: UserLogin,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)):


    """
    Authenticate user and return JWT token
    """

    user_data = UserLogin(
        email=form_data.username,
        password=form_data.password
    )
   
    result = login_user(
        db=db,
        user_data=user_data
    )

    return result

# ---------------------------------------------------
# CURRENT LOGGED-IN USER
# ---------------------------------------------------

@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK
)
def get_me(
    current_user: User = Depends(get_current_user)
):

    """
    Get current authenticated user
    """

    return current_user