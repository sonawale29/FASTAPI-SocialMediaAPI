from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4
from typing import List
from utils.auth_utils import hash_password,verify_password,create_access_token
from db.database import SessionLocal
from db.models import UserModel
from schemas.users_schema import *
from dependencies import get_current_user
# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Initialize router
router = APIRouter()

# GET /users: List all users
@router.get("/users", response_model=List[User])
def list_users(db: Session = Depends(get_db)):
    return db.query(UserModel).all()


# GET /users/{id}: Retrieve a user profile by their ID
@router.get("/users/{id}", response_model=User)
def get_user(id: str, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# POST /users: Create a new user
@router.post("/users", response_model=User, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = UserModel(id=str(uuid4()), name=user.name, email=user.email, password_hash=hash_password(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/users/login/")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Verify the password using utility function
    if not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid password")

    # Create and return a JWT token
    access_token = create_access_token(data={"sub": db_user.email})
    return {"message": "Login successful", "access_token": access_token, "token_type": "bearer"}


# PUT /users/{id}: Update a user's profile by their ID
@router.put("/users/{id}", response_model=User)
def update_user(id: str, user_update: UserUpdate, db: Session = Depends(get_db),
                current_user: dict = Depends(get_current_user)):
    user = db.query(UserModel).filter(UserModel.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user_update.name:
        user.name = user_update.name
    if user_update.email:
        user.email = user_update.email

    db.commit()
    db.refresh(user)
    return user


# DELETE /users/{id}: Delete a user's profile by their ID
@router.delete("/users/{id}")
def delete_user(id: str, db: Session = Depends(get_db),current_user: dict = Depends(get_current_user)):
    user = db.query(UserModel).filter(UserModel.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"detail": "User deleted successfully"}
