from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.core.security import hash_password, verify_password, create_access_token, get_current_user

router=APIRouter()

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user=User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password)
        )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user=db.query(User).filter(User.email==user.email).first()

    if not db_user:
        return {"error": "Invalid email or password"}

    if not verify_password(user.password, db_user.password):
        return {"error": "Invalid email or password"}
    
    token=create_access_token({"user_id": db_user.id})

    return {"access_token": token, "token_type": "bearer"}


@router.get("/profile", response_model=UserResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user