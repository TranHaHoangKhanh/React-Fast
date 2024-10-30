from typing import Union, List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app's address
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Person(BaseModel):
    id: int
    name: str
    age: int
    gender: str

DB: List[Person] = [
    Person(id=1, name="John", age=30, gender="Male"),
    Person(id=2, name="Jane", age=25, gender="Female"),
    Person(id=3, name="Bob", age=35, gender="Male"),
    Person(id=4, name="Alice", age=35, gender="Female"),
    Person(id=5, name="Charlie", age=20, gender="Male"),
    Person(id=6, name="Emily", age=28, gender="Female"),
    Person(id=7, name="Henry", age=30, gender="Male"),
    Person(id=8, name="Ken", age=25, gender="Female"),
    Person(id=9, name="Bob", age=35, gender="Male"),
    Person(id=10, name="Alice", age=35, gender="Female"),
]

@app.get("")
async def root():
    return {"message": "Welcome to my FastAPI application!"}

@app.get("/api")
async def get_persons():
    return DB

@app.get("/item/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}