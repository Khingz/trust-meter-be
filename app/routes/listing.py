from fastapi import APIRouter, status, Depends
from app.services.listing_service import listing_service
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.listing import ListingCreate

listings = APIRouter(prefix="/listings", tags=["Listings"])

@listings.get("/", status_code=status.HTTP_200_OK)
def get_listings(db: Session = Depends(get_db), page: int = 1 ):
    """Endpoint to get all listings"""
    listings = listing_service.get_all(db=db, page=page)

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
def add_listing(schema: ListingCreate, db: Session = Depends(get_db)):
    """Endpoint to add a new listing"""
    new_listing = listing_service.create(db=db, schema=schema)
    response = JSONResponse(
        status_code=201,
        content={
            "status_code": 201,
            "message": "Listing added successfully",
            "data": new_listing
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

    
