from sqlalchemy import create_engine,text
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

from src.core.config import settings

async_engine = AsyncEngine(create_engine(url=settings.DATABASE_URL))

async def init_db() -> None:
    async with async_engine.begin() as conn:
        
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    
    Session = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with Session() as session:
        yield session