"""
Authentication routes and user management
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from utils.security import get_password_hash, verify_password, create_access_token
from utils.schemas import UserCreate, TokenResponse
from utils.dependencies import get_current_user

from db.database import get_db
from db.models import User

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """User registration endpoint."""
    # 检查用户名/邮箱是否已存在 | Check for existing user
    print(1111)
    existing_user = db.query(User).filter(
        (User.user_name == user.username) | (User.email == user.email)
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered."
        )

    # 哈希密码并保存用户 | Hash password & save user
    hashed_password = get_password_hash(user.password)
    new_user = User(
        user_name=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    return {"User registered successfully"}


@router.post("/token", response_model=TokenResponse)
async def login_for_access_token(username: str,password: str,db: Session = Depends(get_db)):
    """Login endpoint returning JWT."""
    user = db.query(User).filter(User.user_name == username).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    #Generate JWT
    access_token = create_access_token(data={"sub": user.user_name})
    return {"access_token": access_token, "token_type": "bearer"}
