from fastapi import FastAPI
from src.routers.router_book import book_router
from src.routers.router_user import user_router
from src.routers.router_review import review_router
from src.routers.router_tag import tag_router
from contextlib import asynccontextmanager
from src.db.database import init_db


@asynccontextmanager
async def life_span(app: FastAPI):
    print(f"server is starting ....")
    await init_db()
    yield 
    print(f"server has been stopped")

version = "v1"

app = FastAPI(
    title="FastAPI App",
    description="A simple FastAPI app",
    version=version
)

app.include_router(book_router)
app.include_router(user_router)
app.include_router(review_router)
app.include_router(tag_router)