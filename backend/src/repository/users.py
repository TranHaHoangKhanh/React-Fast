from sqlalchemy import update as sql_update
from sqlalchemy.future import select

from src.db.database import db, commit_rollback
from src.model.users import Users
from src.repository.base_repo import BaseRepo
from src.model.users import Users
from src.repository.base_repo import BaseRepo

class UsersRepository(BaseRepo):
    model = Users
    
    @staticmethod
    async def find_by_username(username: str):
        query = select(Users).where(Users.username == username)
        return (await db.execute(query)).scalar_one_or_none()
    
    @staticmethod
    async def find_by_email(email:str):
        query = select(Users).where(Users.email == email)
        return (await db.execute(query)).scalar_one_or_none()
    
    @staticmethod
    async def update_password(email: str, password: str):
        query  = sql_update(Users).where(Users.email == email).values(password=password).execution_options(synchronize_session="fetch")
        await db.execute(query)
        await commit_rollback()