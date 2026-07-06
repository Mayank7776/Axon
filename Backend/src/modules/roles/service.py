from sqlalchemy.orm import Session #type: ignore
from src.modules.roles.models import Role
from src.modules.roles.schemas import *
from src.utils.response import Response
from src.modules.users.models import User

def get_all_roles(db: Session):
    roles = db.query(Role).all()
    role_list = []
    for r in roles:
        role_list.append({
            "id": r.id,
            "name": r.name,
            "description": r.description,
            "is_active": r.is_active
        })
    return Response(
        success=True,
        message="Roles retrieved successfully",
        data=role_list
    )

def add_role(body: addRole, db: Session):
    existing_role = db.query(Role).filter(Role.name == body.name).first()
    if existing_role:
        return Response(
            success=False,
            message="Role name already exists",
            data=None
        )
    
    new_role = Role(
        name=body.name,
        description=body.description,
        is_active=body.is_active if body.is_active is not None else True
    )
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    
    return Response(
        success=True,
        message="Role created successfully",
        data={
            "id": new_role.id,
            "name": new_role.name,
            "description": new_role.description,
            "is_active": new_role.is_active
        }
    )

def update_role_by_id(id: str, body: updateRole, db: Session):
    role = db.query(Role).filter(Role.id == id).first()
    if not role:
        return Response(
            success=False,
            message="Role not found",
            data=None
        )
    
    update_data = body.model_dump(exclude_unset=True)
    
    if "name" in update_data:
        existing_name = db.query(Role).filter(
            Role.name == update_data["name"],
            Role.id != id
        ).first()
        if existing_name:
            return Response(
                success=False,
                message="Role name already exists",
                data=None
            )
            
    for field, value in update_data.items():
        setattr(role, field, value)
        
    db.commit()
    db.refresh(role)
    
    return Response(
        success=True,
        message="Role updated successfully",
        data={
            "id": role.id,
            "name": role.name,
            "description": role.description,
            "is_active": role.is_active
        }
    )

def delete_role_by_id(id: str, db: Session):
    role = db.query(Role).filter(Role.id == id).first()
    if not role:
        return Response(
            success=False,
            message="Role not found",
            data=None
        )
    
    # Check if any users are assigned to this role
    user_count = db.query(User).filter(User.role_id == id).count()
    if user_count > 0:
        return Response(
            success=False,
            message="Cannot delete role as it is assigned to users",
            data=None
        )
        
    db.delete(role)
    db.commit()
    
    return Response(
        success=True,
        message="Role deleted successfully",
        data=None
    )
    

