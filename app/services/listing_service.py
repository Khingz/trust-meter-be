from sqlalchemy.orm import Session
from app.schemas.listing import ListingCreate, ListingUpdate
from sqlalchemy.orm import Session
from app.models.listing import Listing
from app.utils.web_scraper import get_name_from_url, get_logo, is_valid_url, ensure_valid_url
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException

class ListingService:
    """ Listing service class """
    def create(self, db: Session, schema):
        """Create a new listing"""
        if not is_valid_url(schema.url):
            raise HTTPException(status_code=400, detail="Invalid URL")
        valid_url = ensure_valid_url(schema.url)
        listing = db.query(Listing).filter(Listing.listing_url == valid_url).first()
        if listing:
            raise HTTPException(status_code=400, detail="Listing already exists")
        name = get_name_from_url(schema.url)
        logo = get_logo(schema.url)

        listing_data = {
            "name": name,
            "description": "Temp description",
            "image": logo,
            "listing_url": valid_url,
        }
        new_listing = Listing(**listing_data)
        db.add(new_listing)
        db.commit()
        db.refresh(new_listing)

        serialized_listing = jsonable_encoder(new_listing)

        return serialized_listing

    
    def update(self, db: Session, schema: ListingUpdate):
        """Update a listing"""
        pass
    
    def delete(self, db: Session, id: int):
        """Delete a listing"""
        pass
    
    def get_all(self, db: Session):
        """Get all listings"""
        listings = db.query(Listing).all()
        serialized_listing = jsonable_encoder(listings)
        return serialized_listing

    
    def get_by_id(self, db: Session, id: int):
        """Get a listing by Id"""
        pass

listing_service = ListingService()