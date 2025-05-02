from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.conf.config import settings

DATABASE_URL = settings.DB_URL.replace("postgresql://", "postgresql+asyncpg://")

engine = create_async_engine(DATABASE_URL, echo=True)

async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
