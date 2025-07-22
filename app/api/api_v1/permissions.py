from fastapi import Depends, APIRouter, status, HTTPException, Request
from sqlalchemy.orm import Session
from app.api import deps
import app.crud.account as accountCrud
from app.schemas.account import CreatePermission, PermissionOut


router = APIRouter()

@router.post("/", response_model=PermissionOut)
def create_permission(data: CreatePermission, db: Session = Depends(deps.get_db)):
    return accountCrud.create_permission(db, data)


@router.get("/", response_model=list[PermissionOut])
def list_permissions(db: Session = Depends(deps.get_db)):
    return accountCrud.get_all_permissions(db)