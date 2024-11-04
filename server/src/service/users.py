from sqlalchemy.future import select
from src.model import Users, Person
from src.db.database import db


class UserService:
    
    @staticmethod
    async def get_user_profile(username: str):
        query = select(Users.username,
                       Users.email,
                       Person.name,
                       Person.birth,
                       Person.sex,
                       Person.profile,
                       Person.phone_number).join_from(Users, Person).where(Users.username == username)
        return(await db.execute(query)).mappings().one()