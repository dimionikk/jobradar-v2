from argon2 import PasswordHasher
from datetime import datetime,timedelta,timezone
from jose import jwt
from app.core.config import settings

ph = PasswordHasher()

def hash_password(password: str) -> str:
    return ph.hash(password)

def verify_password(hashed_password: str, password: str) -> bool:
    return ph.verify(hashed_password, password)

def create_access_token(data:dict)->str:
    to_encode=data.copy()
    expire=datetime.now(timezone.utc)+timedelta(minutes=15)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,settings.JWT_SECRET_KEY,algorithm="HS256")

def decode_access_token(token:str)->dict:
    return jwt.decode(token,settings.JWT_SECRET_KEY,algorithms=["HS256"])