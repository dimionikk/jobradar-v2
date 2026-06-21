from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core import security, database
from app.schemas import user
from app.models import user as user_model
from datetime import datetime, timezone
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(database.get_db)
) -> user_model.User:
    is_blacklisted = await database.redis_client.exists(f"blacklist:{token}")
    if is_blacklisted:
        raise HTTPException(status_code=401, detail="Токен відкликаний")

    payload = security.decode_access_token(token)
    user_id = payload.get("user_id")

    result = await db.execute(select(user_model.User).where(user_model.User.id == user_id))
    current_user = result.scalar_one_or_none()

    if current_user is None:
        raise HTTPException(status_code=401, detail="Користувач не знайдений")

    return current_user

@router.post("/register")
async def register(data: user.UserRegister, db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(user_model.User).where(user_model.User.email == data.email))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email вже існує")

    hashed_password = security.hash_password(data.password)
    new_user = user_model.User(email=data.email, hashed_password=hashed_password)
    db.add(new_user)
    await db.commit()

    return {"status": "registered"}

@router.post("/login", response_model=user.Token)
async def login(data: user.UserRegister, db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(user_model.User).where(user_model.User.email == data.email))
    existing_user = result.scalar_one_or_none()

    if not existing_user or not security.verify_password(existing_user.hashed_password, data.password):
        raise HTTPException(status_code=401, detail="Невірний email або пароль")

    access_token = security.create_access_token({"user_id": existing_user.id})

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
async def logout(token: str):
    payload = security.decode_access_token(token)
    exp_timestamp = payload["exp"]
    now_timestamp = datetime.now(timezone.utc).timestamp()
    ttl_seconds = int(exp_timestamp - now_timestamp)

    await database.redis_client.set(f"blacklist:{token}", "true", ex=ttl_seconds)

    return {"status": "logged out"}