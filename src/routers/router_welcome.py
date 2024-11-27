from fastapi import APIRouter
from fastapi.responses import JSONResponse
from src.core.config import settings
"""
Background tasks for celery
from src.utils.celery_tasks import send_email
"""

welcome_router = APIRouter(
    prefix='',
    tags=["Welcome"]
)
version = "v1"

version_prefix = f'/api/{version}'

link = f"{settings.DOMAIN}/api/v1/docs"
@welcome_router.get('/')
async def root():
    return JSONResponse(
        content={
            "message": "Welcome to FastAPI",
            "version": version,
            "description": f"Please click this link {link} to see the documentation."
        },
        status_code=200
    )

