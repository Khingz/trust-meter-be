from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException

def paginate_query(
    db: Session,
    model,
    page: int = 1,
    page_size: int = 10,
    filters: dict = None,
    search_by: str = None,
    search_term: str = None
):
    query = db.query(model)

    # Apply filters (e.g., {"status": "active"})
    if filters:
        for key, value in filters.items():
            column = getattr(model, key, None)
            if column is not None:
                query = query.filter(column == value)
            else:
                raise HTTPException(status_code=400, detail=f"Invalid filter field: {key}")

    # Apply search
    if search_by and search_term:
        column = getattr(model, search_by, None)
        if column is not None:
            query = query.filter(column.ilike(f"%{search_term}%"))
        else:
            raise HTTPException(status_code=400, detail=f"Invalid search field: {search_by}")

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
