from fastapi import FastAPI, Depends,HTTPException,status
from pydantic import BaseModel

from sqlalchemy.orm import Session
from sqlalchemy import text

from database import engine, SessionLocal
from models import Base, User
import hashlib


app = FastAPI()

class UserCreateRequest(BaseModel):
    username: str
    password: str
    email: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



def get_password_hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest() 

@app.on_event("startup")
async def startup():
    print("Starting up...")
    with engine.begin() as conn:
        table_exists = conn.execute(
            text("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        )
        if not table_exists.scalar():
            Base.metadata.create_all(bind=engine)
            print("Database tables created.")
            

@app.get("/users")
async def read_users(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    return user


@app.post("/add_users/", status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreateRequest,db: Session = Depends(get_db)  
):
    
    existing_user = db.query(User).filter(User.user_name == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered."
        )

    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        user_name=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully", "user_id": new_user.id}
