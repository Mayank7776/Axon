# Skill: Create Service

This skill describes how to write service layer functions in `src/modules/<module_name>/service.py` that handle DB transactions, business logic, pagination, sorting, and filtering.

## Guidelines

1. Service functions should be plain python functions that receive `db: Session` as a parameter.
2. For lists, implement search over textual columns using `ilike` and `or_`.
3. Support pagination using `offset = (filter.page - 1) * filter.limit`.
4. Support dynamic sorting by mapping input sort keys to SQLAlchemy columns.
5. Always wrap return values in `Response(success=bool, message=str, data=any)`.
6. Enforce transaction safety (commit changes and refresh models).

## Template Code

```python
# src/modules/items/service.py
from sqlalchemy.orm import Session
from sqlalchemy import or_
from src.modules.items.models import MyEntity
from src.modules.items.schemas import addMyEntity
from src.utils.datatable import DataTableFilter
from src.utils.response import Response

def get_entities(filter: DataTableFilter, db: Session) -> Response:
    query = db.query(MyEntity)
    
    if filter.search:
        pattern = f"%{filter.search}%"
        query = query.filter(
            or_(
                MyEntity.title.ilike(pattern),
                MyEntity.description.ilike(pattern)
            )
        )
        
    total = query.count()
    
    sort_attr = getattr(MyEntity, filter.sort_by, None)
    if sort_attr is not None:
        if filter.sort_order.lower() == "desc":
            query = query.order_by(sort_attr.desc())
        else:
            query = query.order_by(sort_attr.asc())
    else:
        query = query.order_by(MyEntity.created_at.desc())
        
    offset = (filter.page - 1) * filter.limit
    items = query.offset(offset).limit(filter.limit).all()
    
    serialized = [{
        "id": x.id,
        "title": x.title,
        "created_at": x.created_at
    } for x in items]
    
    return Response(
        success=True,
        message="List retrieved successfully",
        data={
            "items": serialized,
            "total": total,
            "page": filter.page,
            "limit": filter.limit
        }
    )
```
