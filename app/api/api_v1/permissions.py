from fastapi import Depends, APIRouter, status, HTTPException, Request
from sqlalchemy.orm import Session
from app.api import deps
import app.crud.account as accountCrud
from app.schemas.account import CreatePermission, UpdatePermission, PermissionOut


router = APIRouter()

@router.post("/", response_model=PermissionOut)
def create_permission(data: CreatePermission, db: Session = Depends(deps.get_db)):
    return accountCrud.create_permission(db, data)


@router.get("/", response_model=list[PermissionOut])
def list_permissions(db: Session = Depends(deps.get_db)):
    return accountCrud.get_all_permissions(db)


@router.get("/{permission_id}", response_model=PermissionOut)
def get_permission(permission_id: int, db: Session = Depends(deps.get_db)):
    permission = accountCrud.get_permission(db, permission_id)
    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Permission not found"
        )
    return permission


@router.put("/{permission_id}", response_model=PermissionOut)
def update_permission(permission_id: int, data: UpdatePermission, db: Session = Depends(deps.get_db)):
    permission = accountCrud.update_permission(db, permission_id, data)
    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Permission not found"
        )
    return permission


@router.delete("/{permission_id}")
def delete_permission(permission_id: int, db: Session = Depends(deps.get_db)):
    result = accountCrud.delete_permission(db, permission_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Permission not found"
        )
    return {"message": "Permission deleted successfully"}