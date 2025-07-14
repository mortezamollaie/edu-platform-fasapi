from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from app.api import deps
from app.models.user import User

router = APIRouter()

@router.get("/users")
def list_users(db: Session = Depends(deps.get_db)):
    return db.query(User).all()