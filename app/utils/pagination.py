from sqlalchemy.orm import Session, joinedload, RelationshipProperty
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from sqlalchemy.inspection import inspect

def paginate_query(
    db: Session,
    model,
    page: int = 1,
    page_size: int = 30,
    filters: dict = None,
    search_by: str = None,
    search_term: str = None,
    joined_loads: list = None,
    order_by: str = "created_at",
    descending: bool = True
):
    query = db.query(model)
    
    
    if joined_loads:
        for relation in joined_loads:
            query = query.options(joinedload(relation))

    # Apply filters (e.g., {"status": "active"})
    if filters:
        for key, value in filters.items():
            column = getattr(model, key, None)
            if column is not None:
                mapper = inspect(model)
                attr = mapper.attrs.get(key)

                if key in mapper.relationships:
                    # Handle relationships like Review.user.has(id=value)
                    related_model = mapper.relationships[key].mapper.class_
                    primary_key = list(related_model.__table__.primary_key.columns)[0].name
                    query = query.filter(column.has(**{primary_key: value}))
                else:
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
        
    if order_by:
        column = getattr(model, order_by, None)
        if column is not None:
            query = query.order_by(column.desc() if descending else column.asc())
        else:
            raise HTTPException(status_code=400, detail=f"Invalid order_by field: {order_by}")

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
