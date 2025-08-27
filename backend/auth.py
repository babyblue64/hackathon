from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta
from jose import jwt, JWTError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db, User

# env vars

SECRET_KEY = 'my-secret-key'
ALGORITHM = 'HS256'

# pwd utils

pwd_context = CryptContext(schemes=['bcrypt'])

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

# JWT generation function

def generate_access_token(data: dict, expiry_delta: timedelta):
    payload = data.copy()
    expiry = datetime.now(timezone.utc) + (expiry_delta or timedelta(minutes=15))
    payload.update({"exp": expiry})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# Auth depedency

security = HTTPBearer()

def deduce_current_user(token: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    unauthorized_login_error = HTTPException(status_code=401, detail="Authorization failed")
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise unauthorized_login_error
        user = db.query(User).filter(User.Email == email).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise unauthorized_login_error