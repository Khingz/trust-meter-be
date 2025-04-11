from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.reviews import ReviewCreate

reviews = APIRouter(prefix="/reviews", tags=["Reviews"])

@reviews.get("/", status_code=status.HTTP_200_OK)
def get_listings(db: Session = Depends(get_db)):
    """Endpoint to get all Reviews"""
    return {
        "status_code": 200,
        "message": "Reviews fetched successfully",
        "data": {"message": "Listing fetched successfully"}
    }

@reviews.post("/", status_code=status.HTTP_201_CREATED)
def add_listing(schema: ReviewCreate, db: Session = Depends(get_db)):
    """Endpoint to add a new Reviews"""
    return {
        "status_code": 200,
        "message": "Reviews created successfully",
        "data": {"message": "Listing fetched successfully"}
    }

@reviews.get("/{id}", status_code=status.HTTP_200_OK)
def get_listing_by_id(id: str, db: Session = Depends(get_db)):
    """Endpoint to get a review by Id"""
    return {
        "status_code": 200,
        "message": "Review fetched successfully",
        "data": {"message": "Listing fetched successfully"}
    }

    
