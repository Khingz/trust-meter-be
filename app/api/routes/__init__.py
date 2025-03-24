from fastapi import APIRouter

from app.api.routes.auth import auth

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth)