from sqlalchemy.orm import Session, joinedload, RelationshipProperty
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from sqlalchemy.inspection import inspect
import json
from typing import List, Dict, Any, Type
from sqlalchemy.orm.attributes import InstrumentedAttribute




def apply_joins(query, model, joined_loads):
    if not joined_loads:
        return query

    mapper = inspect(model)

    for relation in joined_loads:
        if not isinstance(relation, InstrumentedAttribute):
            raise HTTPException(status_code=400, detail=f"joined_loads must be InstrumentedAttribute, got {type(relation)}")

        # Validate relation belongs to model's attributes
        if relation.key not in mapper.attrs:
            raise HTTPException(status_code=400, detail=f"Invalid join attribute: {relation.key}")

        # Use relation (InstrumentedAttribute) directly in joinedload
        query = query.options(joinedload(relation))

    return query

def apply_filters(query, model, filters: Dict[str, Any]):
    if isinstance(filters, str):
        filters = json.loads(filters)
    
    if not filters:
        return query

    mapper = inspect(model)
    
    for key, value in filters.items():
        if not hasattr(model, key):
            raise HTTPException(status_code=400, detail=f"Invalid filter field: {key}")
        
        column = getattr(model, key)
        
        if key in mapper.relationships:
            # e.g., Review.user.has(id=value)
            related_model = mapper.relationships[key].mapper.class_
            pk = list(related_model.__table__.primary_key.columns)[0].name
            query = query.filter(column.has(**{pk: value}))
        else:
            query = query.filter(column == value)
    
    return query

def apply_search(query, model, search_by: str, search_term: str):
    if not search_by or not search_term:
        return query

    if not hasattr(model, search_by):
        raise HTTPException(status_code=400, detail=f"Invalid search field: {search_by}")

    column = getattr(model, search_by)
    return query.filter(column.ilike(f"%{search_term}%"))


def apply_ordering(query, model, order_by: str, descending: bool = True):
    if not order_by:
        return query

    if not hasattr(model, order_by):
        raise HTTPException(status_code=400, detail=f"Invalid order_by field: {order_by}")

    column = getattr(model, order_by)
    return query.order_by(column.desc() if descending else column.asc())
    

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
          
    query = apply_joins(query, model, joined_loads)
    query = apply_filters(query, model, filters) # Apply filters (e.g., {"status": "active"})
    query = apply_search(query, model, search_by, search_term)
    query = apply_ordering(query, model, order_by, descending)

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
