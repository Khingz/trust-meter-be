from sqlalchemy.orm import Session
from app.schemas.listing import ListingCreate, ListingUpdate
from sqlalchemy.orm import Session
from app.models.listing import Listing
from app.utils.web_scraper import get_name_from_url, get_logo, normalize_and_validate_domain_url, resolve_image_url
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from app.utils.pagination import paginate_query

class ListingService:
    """ Listing service class """
    def create(self, db: Session, schema):
        """Create a new listing"""
        # if not is_valid_url(schema.url):
        #     raise HTTPException(status_code=400, detail="No product with the url")
        valid_url = normalize_and_validate_domain_url(schema.url)
        listing = db.query(Listing).filter(Listing.listing_url == valid_url).first()
        if listing:
            raise HTTPException(status_code=409, detail="Listing already exists")
        name = get_name_from_url(valid_url)
        logo = get_logo(valid_url)
        logo = resolve_image_url(valid_url, logo)

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
    
    def get_all(self, db: Session, page):
        """Get all listings"""
        return paginate_query(db, model=Listing, page=page)

    
    def get_by_id(self, db: Session, id: str):
        """Get a listing by Id"""
        listing = db.query(Listing).filter(Listing.id == id).first()
        if not listing:
            raise HTTPException(status_code=404, detail="Listing not found")
        return jsonable_encoder(listing)

listing_service = ListingService()