from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    mobile: int
    password: str
    confirm_password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserReturn(BaseModel):
    id: int
    username: str
    email: EmailStr
    hashed_password: str
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True