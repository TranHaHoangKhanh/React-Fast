from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from src.core.config import settings

DATABASE_URL =  f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOSTNAME}:{settings.DATABASE_PORT}/{settings.POSTGRES_DB}"

class AsyncDatabaseSession:
    def __init__(self):
        self.__session__ = None
        self.__engine__ = None
    
    def __getattr__(self, name):
        return getattr(self.__session__, name)
    
    def init(self):
        self.__engine__ = create_async_engine(DATABASE_URL,
                                            future=True,
                                            echo=True)  # Set to False in production
        self.__session__ = sessionmaker(
            self.__engine__, 
            expire_on_commit=False, 
            class_=AsyncSession
        )()
    
    @property
    def engine(self):
        return self.__engine__
        
    async def create_all(self):
        async with self.__engine__.begin() as conn:  # Changed from self.engine to self.__engine__
            await conn.run_sync(SQLModel.metadata.create_all)
            
db = AsyncDatabaseSession()

async def commit_rollback():
    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise