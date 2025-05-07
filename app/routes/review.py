from fastapi import APIRouter, status, Depends, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.reviews import ReviewCreate
from typing import Optional
from app.services.review_service import review_service
from fastapi.responses import JSONResponse
from app.utils.auth import verify_access_token
import json



reviews = APIRouter(prefix="/reviews", tags=["Reviews"])

@reviews.get("/", status_code=status.HTTP_200_OK)
def get_reviews(db: Session = Depends(get_db), page: int = Query(1, ge=1), page_size: int = Query(30), search_by: Optional[str] = Query(None), search_term: Optional[str] = Query(None), filters = Query({}) ):
    """Endpoint to get all Reviews"""
    filters_dict = json.loads(filters) if filters else {}
    listings = review_service.get_all(db=db, page=page, page_size=page_size, search_by=search_by, search_term=search_term, filters=filters_dict)
    
    response = JSONResponse(
        status_code=200,
        content={
            "status_code": 200,
            "message": "Listings fetched successfully",
            "data": listings
        },
    )
    return response

@reviews.post("/", status_code=status.HTTP_201_CREATED)
def add_review(schema: ReviewCreate, db: Session = Depends(get_db), current_user: dict = Depends(verify_access_token)):
    """Endpoint to add a new Reviews"""
    print(current_user.id)
    review = review_service.create(db=db, schema=schema, user_id=current_user.id)
    response = JSONResponse(
        status_code=201,
        content={
            "status_code": 201,
            "message": "Review added successfully",
            "data": review
        }
    )
    return response

@reviews.get("/{id}", status_code=status.HTTP_200_OK)
def get_review_by_id(id: str, db: Session = Depends(get_db)):
    """Endpoint to get a review by Id"""
    return {
        "status_code": 200,
        "message": "Review fetched successfully",
        "data": {"message": "Listing fetched successfully"}
    }

