from fastapi import Depends, APIRouter, status, HTTPException, Request
from sqlalchemy.orm import Session
from app.api import deps
import app.crud.account as accountCrud
from app.schemas.account import CreateRole, UpdateRole, AssignPermissions, RoleOut, PermissionName


router = APIRouter()


@router.post("/", response_model=RoleOut)
def create_role(role_data: CreateRole, db: Session = Depends(deps.get_db)):
    return accountCrud.create_role(db, role_data)


@router.get("/", response_model=list[RoleOut])
def list_roles(db: Session = Depends(deps.get_db)):
    return accountCrud.get_all_roles(db)


@router.get("/{role_id}", response_model=RoleOut)
def get_role(role_id: int, db: Session = Depends(deps.get_db)):
    role = accountCrud.get_role(db, role_id)
    if not role:
        raise HTTPException(404, detail="Role not found")
    return role


@router.put("/{role_id}", response_model=RoleOut)
def update_role(role_id: int, data: UpdateRole, db: Session = Depends(deps.get_db)):
    role = accountCrud.update_role(db, role_id, data)
    if not role:
        raise HTTPException(404, detail="Role not found")
    return role


@router.delete("/{role_id}")
def delete_role(role_id: int, db: Session = Depends(deps.get_db)):
    if not accountCrud.delete_role(db, role_id):
        raise HTTPException(404, detail="Role not found")
    return {"message": "Role deleted"}


@router.post("/{role_id}/permissions", response_model=RoleOut)
def assign_permissions_to_role(role_id: int, data: AssignPermissions, db: Session = Depends(deps.get_db)):
    """Replace all permissions for a role with new ones"""
    role = accountCrud.assign_permissions_to_role(db, role_id, data.permission_ids)
    if not role:
        raise HTTPException(404, detail="Role not found")
    return role


@router.post("/{role_id}/permissions/add", response_model=RoleOut)
def add_permissions_to_role(role_id: int, data: AssignPermissions, db: Session = Depends(deps.get_db)):
    """Add new permissions to existing permissions of a role"""
    role = accountCrud.add_permissions_to_role(db, role_id, data.permission_ids)
    if not role:
        raise HTTPException(404, detail="Role not found")
    return role


@router.post("/{role_id}/permissions/remove", response_model=RoleOut)
def remove_permissions_from_role(role_id: int, data: AssignPermissions, db: Session = Depends(deps.get_db)):
    """Remove specific permissions from a role"""
    role = accountCrud.remove_permissions_from_role(db, role_id, data.permission_ids)
    if not role:
        raise HTTPException(404, detail="Role not found")
    return role


@router.get("/{role_id}/permissions", response_model=list[PermissionName])
def get_role_permissions(role_id: int, db: Session = Depends(deps.get_db)):
    """Get list of permission names for a specific role"""
    permissions = accountCrud.get_role_permissions(db, role_id)
    if permissions is None:
        raise HTTPException(404, detail="Role not found")
    return permissions