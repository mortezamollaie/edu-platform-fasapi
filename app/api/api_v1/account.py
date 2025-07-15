from fastapi import Depends, APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.account import SignUp, SignUpResponse, SendOtp, VerifyOtp
from app.models.user import User
from app.models.account import OtpCode
from app.services.hash_password import Hash
from datetime import datetime, timedelta
from app.services.generate_token import create_access_token
import random

router = APIRouter()

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


@router.post("/verify-otp", status_code=200, tags=["Accounts"])
def verify_otp(request: VerifyOtp, db: Session = Depends(deps.get_db)):
    otp_record = db.query(OtpCode).filter(OtpCode.phone_number == request.phone_number).first()

    if not otp_record:
        raise HTTPException(status_code=404, detail="OTP code not found.")
    
    if otp_record.code != request.code:
        raise HTTPException(status_code=400, detail="Incorrect OTP code.")
    
    time_diff = datetime.utcnow() - otp_record.created_at
    if time_diff > timedelta(minutes=2):
        raise HTTPException(status_code=400, detail="OTP code has expired.")

    db.delete(otp_record)
    db.commit()

    access_token = create_access_token(data={"sub": request.phone_number})
    return {"access_token": access_token, "token_type": "bearer"}        