from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware


origins = [
    "http://localhost:3000",
    ]

app = FastAPI(
    title="React Fast API",
    description="This is my application",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter()

@router.get("/")
def read_root():
    return {"Hello": "World"}
    
app.include_router(router)