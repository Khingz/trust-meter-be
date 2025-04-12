from fastapi import APIRouter, status, Depends, Query
from app.services.listing_service import listing_service
from app.services.review_service import review_service
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.listing import ListingCreate
from typing import Optional
from app.utils.auth import verify_access_token

listings = APIRouter(prefix="/listings", tags=["Listings"])

@listings.get("/", status_code=status.HTTP_200_OK)
def get_listings(db: Session = Depends(get_db), page: int = Query(1, ge=1), search_by: Optional[str] = Query(None), search_term: Optional[str] = Query(None)):
    """Endpoint to get all listings"""
    listings = listing_service.get_all(db=db, page=page, search_by=search_by, search_term=search_term)

    response = JSONResponse(
        status_code=200,
        content={
            "status_code": 200,
            "message": "Listings fetched successfully",
            "data": listings
        },
    )
    return response

@listings.post("/", status_code=status.HTTP_201_CREATED)
def add_listing(schema: ListingCreate, db: Session = Depends(get_db), current_user: dict = Depends(verify_access_token)):
    """Endpoint to add a new listing"""
    listing = listing_service.create(db=db, schema=schema)
    response = JSONResponse(
        status_code=201,
        content={
            "status_code": 201,
            "message": "Listing added successfully",
            "data": listing
        }
    )
    return response

@listings.get("/{id}", status_code=status.HTTP_200_OK)
def get_listing_by_id(id: str, db: Session = Depends(get_db)):
    """Endpoint to get a listing by Id"""
    listing = listing_service.get_by_id(db=db, id=id)
    response = JSONResponse(
        status_code=200,
        content={
            "status_code": 200,
            "message": "Listing fetched successfully",
            "data": listing
        }
    )
    return response

@listings.get("/{listing_id}/reviews/stats")
def get_reviews_stats(listing_id, db: Session = Depends(get_db)):
    stats = review_service.get_listing_review_stats(db=db, listing_id=listing_id)
    response = JSONResponse(
        status_code=200,
        content={
            "status_code": 200,
            "message": "Stats fetched successfully",
            "data": stats
        }
    )
    return response 
