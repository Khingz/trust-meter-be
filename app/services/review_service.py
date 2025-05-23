from sqlalchemy.orm import Session
from app.models.review import Review
from app.models.comment import ReviewComment
from app.models.like import Like
from app.schemas.reviews import ReviewUpdate
from app.utils.pagination import paginate_query
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from uuid import UUID
from app.models.review import Review
from sqlalchemy import func
from decimal import Decimal


class ReviewService:
    """ Review service class """
    def create(self, db: Session, schema, user_id: UUID):
        review = Review(
            user_id=user_id,
            listing_id=schema.listing_id,
            comment=schema.comment,
            rating=schema.rating
        )
        
        db.add(review)
        db.commit()
        db.refresh(review)
        
        return jsonable_encoder(review)

    
    def update(self, db: Session, schema: ReviewUpdate):
        """Update a review"""
        pass
    
    def delete(self, db: Session, id: int):
        """Delete a review"""
        pass
    
    def get_all(self, db: Session, page, page_size, search_by, search_term, filters):
        """Get all reviews"""
        return paginate_query(db, model=Review, page=page, page_size=page_size, search_by=search_by, search_term=search_term, filters=filters, joined_loads=[Review.listings, Review.user])
    
    def get_by_id(self, db: Session, id: str):
        """Get a review by Id"""
        listing = db.query(Review).filter(Review.id == id).first()
        if not listing:
            raise HTTPException(status_code=404, detail="Listing not found")
        return jsonable_encoder(listing)
    
    def get_listing_review_stats(self, db: Session, listing_id: UUID):
        total_reviews = db.query(func.count(Review.id)).filter(Review.listing_id == listing_id).scalar()
        average_rating = db.query(func.avg(Review.rating)).filter(Review.listing_id == listing_id).scalar()
        
        if isinstance(average_rating, Decimal):
            average_rating = round(float(average_rating), 2)
        
        rating_counts = {}
        for rating in range(1, 6):
            count = db.query(func.count(Review.id)).filter(Review.listing_id == listing_id, Review.rating == rating).scalar()
            rating_counts[rating] = count
        
        return {
            "total_reviews": total_reviews,
            "average_rating": average_rating if average_rating else 0,
            "rating_counts": rating_counts
        }
        
    def toggle_like(self, db: Session, target_id: int, user_id: UUID):
        """Like or unlike a review"""
        existing = db.query(Like).filter_by(user_id=user_id, target_id=target_id).first()
        if existing:
            db.delete(existing)
            db.commit()
            return {"message": "Unliked"}
        else:
            like = Like(user_id=user_id, target_id=target_id, target_type="review")
            db.add(like)
            db.commit()
            return {"message": "Liked"}
        
    def add_comment(self, db: Session, review_id: str, schema, user_id: str):
        """Add a comment to a review"""
        review = db.query(Review).filter(Review.id == review_id).first()
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")
        
        comment = ReviewComment(
            user_id=user_id,
            review_id=review_id,
            content=schema.content
        )
        
        db.add(comment)
        db.commit()
        db.refresh(comment)
        
        return jsonable_encoder(comment)

review_service = ReviewService()