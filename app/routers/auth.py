# app/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.schemas import UserCreate, UserResponse, TokenPair, UserLogin
from app.models.models import User
from app.utils.security import (
    hash_password, verify_password, create_access_token, create_refresh_token
)
from app.utils.dependencies import db_dep, current_user_dep, get_db
from uuid import uuid4
from fastapi.security import OAuth2PasswordRequestForm



router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=201)
def register(user_data: UserCreate, db: db_dep):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(user_data.password)

    new_user = User(
        email=user_data.email,
        username=user_data.username,
        password_hash=hashed_pw,
        is_active=True,
        is_verified=False,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    #email verify link yuborish
    token = str(uuid4())  
    
    return new_user





@router.post("/login", response_model=TokenPair)
def login(form_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.email).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": user.email})
    refresh_token = create_refresh_token({"sub": user.email})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }










@router.get("/me", response_model=UserResponse)
def get_me(user: current_user_dep):
    return user




@router.post("/verify-email/{token}")
def verify_email(token: str, db: db_dep):
    ...
    return {"msg": "Email verified successfully"}



