from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.schemas import UserResponse, UserCreate
from app.models.models import User
from app.utils.dependencies import db_dep, current_user_dep
from typing import List

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserResponse)
def get_me(user: current_user_dep):
    return user

@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, db: db_dep):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/", response_model=List[UserResponse])
def get_all_users(db: db_dep):
    return db.query(User).all()


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: db_dep):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
