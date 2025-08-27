from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, User, Role
from auth import hash_password, verify_password, generate_access_token, deduce_current_user
from validation import UserCreate, UserLogin, UserReturn
from typing import cast
from datetime import timedelta
from fastapi.middleware.cors import CORSMiddleware
import os
from fastapi.responses import FileResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"]
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_PATH = os.path.join(BASE_DIR, "../frontend", "index.html")

@app.get("/")
async def serve_index():
    return FileResponse(INDEX_PATH)

@app.get('/health')
def health_check():
    return {"status": "running"}

# SIGN UP
@app.post('/auth/signup')
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    if db.query(User).filter(User.Name == user.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")

    if db.query(User).filter(User.Email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    if db.query(User).filter(User.Mobile == str(user.mobile)).first():
        raise HTTPException(status_code=400, detail="Mobile number already registered")

    role_obj = db.query(Role).filter(Role.RoleName == "Citizen").first()
    if not role_obj:
        raise HTTPException(status_code=500, detail="Default role not found")

    new_user = User(
        Name=user.username,
        Email=user.email,
        Mobile=str(user.mobile),
        PasswordHash=hash_password(user.password),
        Role=role_obj.RoleID
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"user_id": new_user.UserID, "detail": "New user registered"}

# LOG IN
@app.post('/auth/login')
def issue_access_token(user: UserLogin, db: Session = Depends(get_db)):
    saved_user = db.query(User).filter(User.Email == user.email).first()
    if not saved_user:
        raise HTTPException(status_code=404, detail="Email not found")

    if not verify_password(user.password, cast(str, saved_user.PasswordHash)):
        raise HTTPException(status_code=401, detail="Incorrect password")

    token = generate_access_token({"sub": user.email}, timedelta(minutes=30))
    return {"access_token": token, "token_type": "Bearer"}


# PROFILE ROUTE (PROTECTED)
@app.get("/users/me", response_model=UserReturn)
def read_user_details(user: User = Depends(deduce_current_user)):
    return user