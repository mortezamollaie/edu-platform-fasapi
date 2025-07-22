from fastapi import Depends, APIRouter, status, HTTPException, Request
from sqlalchemy.orm import Session
from app.api import deps
import app.crud.account as accountCrud
from app.schemas.account import CreateRole, RoleOut


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
def update_role(role_id: int, data: CreateRole, db: Session = Depends(deps.get_db)):
    role = accountCrud.update_role(db, role_id, data)
    if not role:
        raise HTTPException(404, detail="Role not found")
    return role


@router.delete("/{role_id}")
def delete_role(role_id: int, db: Session = Depends(deps.get_db)):
    if not accountCrud.delete_role(db, role_id):
        raise HTTPException(404, detail="Role not found")
    return {"message": "Role deleted"}