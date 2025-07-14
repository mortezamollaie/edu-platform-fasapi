from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.account import SignUp
from app.models.user import User
import random

router = APIRouter()

@router.post("/signup")
def signup(request: SignUp, db: Session = Depends(deps.get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        user = User(email=request.email, first_name=request.first_name, last_name=request.last_name, password=request.password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    return {"error": "a user with this email already exists."}
