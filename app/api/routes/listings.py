from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.product import ProductCreate, ProductResponse
from app.services.product_service import create_product_service
from app.db.session import get_db

router = APIRouter()

@router.post("/products", response_model=ProductResponse, status_code=201)
def create_product_endpoint(
    product_data: ProductCreate,
    db: Session = Depends(get_db)
):
    """
    Endpoint to create a new product listing.
    Validates input, checks for duplicates, and saves the product.
    """
    return create_product_service(db, product_data)
