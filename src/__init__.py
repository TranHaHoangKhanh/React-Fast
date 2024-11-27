from fastapi import FastAPI
from src.routers.router_welcome import welcome_router
from src.routers.router_book import book_router
from src.routers.router_user import user_router
from src.routers.router_review import review_router
from src.routers.router_tag import tag_router
from src.utils.error_handling import register_all_errors
from src.core.middleware import register_middleware


version = "v1"

description = """
A REST API for a book review web service

This REST API is able to: \n
_ Create, Read, Update, Delete books. \n
_ Create, Read, Update, Delete users. \n
_ Create, Read, Delete reviews (include book, rating). \n
_ Create, Read, Update, Delete tags (include to add tags to books). \n
"""


version_prefix = f'/api/{version}'

app = FastAPI(
    title="FastAPI App",
    description=description,
    version=version,
    license_info={"name": "MIT License", "url": "https://opensource.org/license/mit\n"},
    contact={
        "url": "https://github.com/TranHaHoangKhanh",
        "name": "Hoang Khanh",
        "email": "khanhoanghatran@gmail.com"
    },
    openapi_url=f'{version_prefix}/openapi.json',
    docs_url=f'{version_prefix}/docs',
    redoc_url=f'{version_prefix}/redoc'
)


register_all_errors(app)

register_middleware(app)



app.include_router (welcome_router)
app.include_router(book_router)
app.include_router(user_router)
app.include_router(review_router)
app.include_router(tag_router)