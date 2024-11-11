from typing import Generic, TypeVar
from sqlalchemy import update as sql_update, delete as sql_delete
from sqlalchemy.future import select
from src.db.database import db, commit_rollback

T = TypeVar('T')

class BaseRepo:
    model = Generic[T]
    
    @classmethod
    async def create(cls, **kwargs):
            model_instance = cls.model(**kwargs)  # Create instance with kwargs
            db.add(model_instance)
            await db.commit()
            await db.refresh(model_instance)
            return model_instance
        
    @classmethod
    async def get_all(cls):
        query = select(cls.model)
        return (await db.execute(query)).scalars().all()
    
    async def get_by_id(cls, model_id: str):
        query = select(cls.model).where(cls.model.id == model_id)
        return (await db.execute(query)).scalars()
    
    @classmethod
    async def update(cls, model_id: str, **kwargs):
        query = select(cls.model).where(cls.model.id == model_id).values(**kwargs).execution_options(synchronize_session="fetch")
        await db.execute(query)
        await commit_rollback()
        
    async def delete(cls, model_id: str):
        query = sql_delete(cls.model).where(cls.model.id == model_id)
        await db.execute(query)
        await commit_rollback()
    