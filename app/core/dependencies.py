from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core import security, database
from app.models import user as user_model

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