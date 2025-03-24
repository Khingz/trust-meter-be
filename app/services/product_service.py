from sqlalchemy.orm import Session
from app.db import crud
from app.schemas.product import ProductCreate, ProductUpdate
from app.utils.web_scraper import scrape_product_details

# Search for a product by name or URL
def search_product(db: Session, name: str = None, url: str = None):
    if name:
        return crud.get_product_by_name(db, name)
    # Search by URL using web scraping
    if url:
        product_details = scrape_product_details(url)
        if product_details:
            return product_details
    return None

# Create a new product
def create_product(db: Session, product: ProductCreate):
    return crud.create_product(db, product)

# Update an existing product
def update_product(db: Session, product_id: int, product_update: ProductUpdate):
    db_product = crud.get_product(db, product_id)
    if db_product:
        return crud.update_product(db, db_product, product_update)
    return None

# Delete a product by ID
def delete_product(db: Session, product_id: int):
    return crud.delete_product(db, product_id)