from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from .config import settings
from sqlalchemy.orm import DeclarativeBase
import redis.asyncio as redis

engine = create_async_engine(settings.DATABASE_URL)

AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

        