from datetime import date
from typing import Optional
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship
from src.model.mixins import TimeMixin
class Sex(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"


class Person(SQLModel, TimeMixin,table=True):
    __tablename__ = "person"

    id: Optional[str] = Field(None, primary_key=True, nullable=False)
    name: str
    birth: date
    sex: Sex
    profile: str
    phone_number: str

    users: Optional["Users"] = Relationship(
        sa_relationship_kwargs={'uselist': False}, 
        back_populates="person"
    )