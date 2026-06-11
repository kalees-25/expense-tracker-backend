import logging
from datetime import timedelta

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from core.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    hash_password,
    verify_password,
)
from models.users import User
from schemas.auth import UserCreate, UserLogin, UserResponse

logger = logging.getLogger(__name__)


def normalize_email(email: str) -> str:
    return email.strip().lower()


def normalize_username(username: str) -> str:
    return username.strip()


def register_user(db: Session, user_data: UserCreate) -> User:
    
    email = normalize_email(user_data.email)
    
    username = normalize_username(user_data.username)
    

    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        
        logger.warning("Register failed: email already exists -> %s", email)
        
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )

    existing_username = db.query(User).filter(User.username == username).first()
    if existing_username:
        
        logger.warning("Register failed: username already exists -> %s", username)
        
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )

    new_user = User(
        username=username,
        
        email=email,
        
        hashed_password=hash_password(user_data.password)
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        logger.info("User registered successfully -> id=%s, email=%s", new_user.id, new_user.email)
        return new_user

    except IntegrityError:
        db.rollback()
        logger.exception("DB integrity error while registering user -> email=%s", email)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )

    except Exception:
        db.rollback()
        logger.exception("Unexpected error while registering user -> email=%s", email)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong while registering user"
        )

# ---------------
def login_user(db: Session, user_data: UserLogin):
    email = normalize_email(user_data.email)

    user = db.query(User).filter(User.email == email).first()

    if not user:
        logger.warning("Login failed: user not found -> %s", email)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    if not verify_password(user_data.password, user.hashed_password):
        logger.warning("Login failed: wrong password -> %s", email)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "email": user.email
        },
        expires_delta=access_token_expires
    )

    logger.info("User logged in successfully -> id=%s, email=%s", user.id, user.email)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.model_validate(user)
    }