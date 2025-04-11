from fastapi import APIRouter

from app.routes.auth import auth
from app.routes.listing import listings
from app.routes.review import reviews

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth)
api_router.include_router(listings)
api_router.include_router(reviews)