from fastapi import Depends, APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.account import SignUp, SignUpResponse
from app.models.user import User
from app.services.hash_password import Hash

router = APIRouter()

@router.post("/signup", response_model=SignUpResponse, status_code=status.HTTP_201_CREATED)
def signup(request: SignUp, db: Session = Depends(deps.get_db)):
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="a user with this email already exists.")
    hash_password = Hash.bcrypt(request.password)
    user = User(email=request.email, first_name=request.first_name, last_name=request.last_name, password=hash_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
