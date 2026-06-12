from sqlalchemy.orm import Session #type: ignore
from sqlalchemy import or_ #type: ignore
from src.models.user_model import User
from src.models.role_model import Role
from src.schemas.user_schema import *
from src.utils.datatable import DataTableFilter
from src.utils.response import Response
from pwdlib import PasswordHash #type:ignore
from pwdlib.hashers.argon2 import Argon2Hasher #type:ignore

_password_hash = PasswordHash([Argon2Hasher()])

def _hash_password(password: str) -> str:
    return _password_hash.hash(password)

def get_all_users(filter: DataTableFilter, db: Session):
    # Perform outer join with Role to allow searching and sorting on role columns
    query = db.query(User).outerjoin(Role)
    
    # Searching across User fields (username, email, id, role_id) and Role name
    if filter.search:
        search_pattern = f"%{filter.search}%"
        query = query.filter(
            or_(
                User.username.ilike(search_pattern),
                User.email.ilike(search_pattern),
                User.role_id.ilike(search_pattern),
                Role.name.ilike(search_pattern)
            )
        )
        
    # Get total count before pagination limits
    total_count = query.count()
    
    # Sort mapping to handle frontend column names like 'name' or 'role'
    sort_mapping = {
        "username": User.username,
        "email": User.email,
        "role": Role.name,           # 'role' or 'role_name' maps to Role.name
        "created_at": User.created_at,
        "updated_at": User.updated_at
    }
    
    # Get sort column from mapping or try direct model attribute
    sort_column = None
    if filter.sort_by:
        sort_by_lower = filter.sort_by.lower()
        sort_column = sort_mapping.get(sort_by_lower)
        if sort_column is None:
            sort_column = getattr(User, filter.sort_by, None)
            
    if sort_column is not None:
        if filter.sort_order.lower() == "desc":
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(User.created_at.desc())
        
    # Pagination
    offset = (filter.page - 1) * filter.limit
    users = query.offset(offset).limit(filter.limit).all()
    
    user_list = []
    for u in users:
        user_list.append({
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "role_id": u.role_id,
            "role_name": u.role.name if u.role else None,
            "created_at": u.created_at,
            "updated_at": u.updated_at
        })
        
    return Response(
        success=True,
        message="Users list retrieved successfully",
        data={
            "items": user_list,
            "total": total_count,
            "page": filter.page,
            "limit": filter.limit
        }
    )

def get_user_by_id(id: str, db: Session):
    user = db.query(User).filter(User.id == id).first()
    
    if not user:
        return Response(
            success=False,
            message="User not found",
            data=None
        )
        
    data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role_id": user.role_id,
        "role_name": user.role.name if user.role else None,
        "created_at": user.created_at,
        "updated_at": user.updated_at
    }
    
    return Response(
        success=True,
        message="User retrieved successfully",
        data=data
    )

def add_user(body: addUser, db: Session):
    existing_user = db.query(User).filter(
        or_(
            User.username == body.username,
            User.email == body.email
        )
    ).first()
    
    if existing_user:
        return Response(
            success=False,
            message="Username or email already exists",
            data=None
        )
    
    new_user = User(
        username=body.username,
        email=body.email,
        hashed_password=_hash_password(body.password),
        role_id=body.role_id
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return Response(
        success=True,
        message="User created successfully",
        data={
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
            "role_id": new_user.role_id,
            "role_name": new_user.role.name if new_user.role else None,
            "created_at": new_user.created_at,
            "updated_at": new_user.updated_at
        }
    )

def update_user_by_id(id: str, body: updateUser, db: Session):

    user = db.query(User).filter(
        User.id == id
    ).first()

    if not user:
        return Response(
            success=False,
            message="User not found",
            data=None
        )

    update_data = body.model_dump(
        exclude_unset=True
    )

    if "email" in update_data:
        existing_email = db.query(User).filter(
            User.email == update_data["email"],
            User.id != id
        ).first()

        if existing_email:
            return Response(
                success=False,
                message="Email already exists",
                data=None
            )

    if "username" in update_data:
        existing_username = db.query(User).filter(
            User.username == update_data["username"],
            User.id != id
        ).first()

        if existing_username:
            return Response(
                success=False,
                message="Username already exists",
                data=None
            )

    if "role_id" in update_data:
        role = db.query(Role).filter(
            Role.id == update_data["role_id"]
        ).first()

        if not role:
            return Response(
                success=False,
                message="Role not found",
                data=None
            )

    for field, value in update_data.items():
        if field == "password":
            user.hashed_password = _hash_password(value)
        else:
            setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return Response(
        success=True,
        message="User updated successfully",
        data={
            "id": user.id
        }
    )

def delete_user_by_id(id: str, db: Session):
    existing_user = db.query(User).filter(User.id == id).first()
    
    if not existing_user:
        return Response(
            success=False,
            message="User not found",
            data=None
        )
        
    db.delete(existing_user)
    db.commit()
    
    return Response(
        success=True,
        message="User deleted successfully",
        data=None   
    )

    

