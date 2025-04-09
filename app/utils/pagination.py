from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

def paginate_query(
    db: Session,
    model,
    page: int = 1,
    page_size: int = 10,
    filters=None
):
    query = db.query(model)

    if filters:
        for key, value in filters.items():
            query = query.filter(getattr(model, key) == value)

    total_count = query.count()
    total_pages = (total_count + page_size - 1) // page_size
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    serialized_listing = jsonable_encoder(items)

    return {
        "data": serialized_listing,
        "page": page,
        "page_size": page_size,
        "total_count": total_count,
        "total_pages": total_pages,
    }

