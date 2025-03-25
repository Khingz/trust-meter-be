from fastapi import APIRouter

from app.routes.auth import auth
from app.routes.listing import listings

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth)
api_router.include_router(listings)