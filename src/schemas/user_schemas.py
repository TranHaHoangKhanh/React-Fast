import uuid
from datetime import datetime
from pydantic import BaseModel, Field
from typing import List

from src.schemas.book_schemas import Book
from src.schemas.review_schemas import ReviewModel

class UserCreateModel(BaseModel):
    firstname: str = Field(max_length=25)
    lastname: str = Field(max_length=25)
    username: str = Field(max_length=12)
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)

class UserModel(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    firstname: str
    lastname: str
    is_verified: bool
    password_hash: str = Field(exclude=True)
    created_at: datetime
    updated_at: datetime

class UserBooksModel(UserModel):
    books: List[Book]
    reviews: List[ReviewModel]
    
    
class UserLoginModel(BaseModel):
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)