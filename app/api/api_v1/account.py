from fastapi import Depends, APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.account import SignUp, SignUpResponse, SendOtp
from app.models.user import User
from app.models.account import OtpCode
from app.services.hash_password import Hash
from datetime import datetime, timedelta
import random

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


@router.post("/send-otp", status_code=status.HTTP_200_OK, tags=["Accounts"])
def sendOtp(request: SendOtp, db: Session = Depends(deps.get_db)):
    existing_otp_code = db.query(OtpCode).filter(OtpCode.phone_number == request.phone_number).first()
    if existing_otp_code:
        time_diff = datetime.utcnow() - existing_otp_code.created_at
        if time_diff < timedelta(minutes=2):
            raise HTTPException(status_code=400, detail="The previous code is still valid. Please wait a moment.")
        else:
            db.delete(existing_otp_code)
            db.commit()

    code = str(random.randint(100000, 999999))
    new_otp = OtpCode(phone_number=request.phone_number, code=code, created_at=datetime.utcnow())
    # TODO : remove this part after sending code via sms.
    print(code)
    db.add(new_otp)
    db.commit()
    db.refresh(new_otp)
    return {"data": "The OTP code was sent successfully."}        