from typing import List, Optional
from sqlmodel import Relationship, SQLModel, Field
from src.model.user_role import UsersRole

from src.model.mixins import TimeMixin 

class Role(SQLModel, TimeMixin, table=True):
    __tablename__ = "role"

    id: Optional[str] = Field(None,primary_key=True, nullable=True)
    role_name: str

    users: List["Users"] = Relationship(back_populates="roles", link_model=UsersRole)
