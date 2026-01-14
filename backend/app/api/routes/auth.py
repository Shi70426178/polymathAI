from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db.database import SessionLocal
from app.db.models import User
from app.utils.security import hash_password, verify_password
from app.utils.jwt import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

# ---------------------
# DB Dependency
# ---------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------
# Request Schema
# ---------------------
class SignupRequest(BaseModel):
    username: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str



# ---------------------
# Signup
# ---------------------
@router.post("/signup")
def signup(body: SignupRequest, db: Session = Depends(get_db)):

    if db.query(User).filter(User.email == body.email).first():
        raise HTTPException(400, "Email already registered")

    if db.query(User).filter(User.username == body.username).first():
        raise HTTPException(400, "Username already taken")

    user = User(
        username=body.username,
        email=body.email,
        hashed_password=hash_password(body.password)
    )

    db.add(user)
    db.commit()

    return {"message": "User created successfully"}

# ---------------------
# Login
# ---------------------
@router.post("/login")
def login(body: LoginRequest, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == body.email).first()

    if not user or not verify_password(body.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "sub": str(user.id),
        "username": user.username
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }
