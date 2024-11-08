from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.db.database import db
from src.service.auth_service import generate_role


origins = [
    "http://localhost:3000",
    ]

def init_app():
    db.init()

    app = FastAPI(
        title= "React FastApi App",
        description= "This is a React FastApi App with basic function",
        version= "0.1.0"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    @app.on_event("startup")
    async def starup():
        await db.create_all()
        await generate_role()
    
    @app.on_event("shutdown")
    async def shutdown():
        await db.close()

    from src.controller import authentication, users

    app.include_router(authentication.router)
    app.include_router(users.router)

    return app

app = init_app()
