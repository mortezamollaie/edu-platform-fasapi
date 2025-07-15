from fastapi import Depends, APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.account import SendOtp, VerifyOtp
from app.services import token_management_service as Token
from app.crud import account as AccountCrud
import random

router = APIRouter()

@router.post("/send-otp", status_code=status.HTTP_200_OK, tags=["Accounts"])
def send_otp(request: SendOtp, db: Session = Depends(deps.get_db)):
    existing_otp = AccountCrud.get_otp_by_phone(db, request.phone_number)

    if existing_otp:
        if not AccountCrud.is_otp_expired(existing_otp):
            raise HTTPException(status_code=400, detail="The previous code is still valid. Please wait a moment.")
        AccountCrud.delete_otp(db, existing_otp)

    code = str(random.randint(100000, 999999))
    print(code)  # ⚠️ برای production حذف شود
    AccountCrud.create_otp(db, request.phone_number, code)

    return {"data": "The OTP code was sent successfully."}


@router.post("/verify-otp", status_code=200, tags=["Accounts"])
def verify_otp(request: VerifyOtp, db: Session = Depends(deps.get_db)):
    otp_record = AccountCrud.get_otp_by_phone(db, request.phone_number)

    if not otp_record:
        raise HTTPException(status_code=404, detail="OTP code not found.")

    if otp_record.code != request.code:
        raise HTTPException(status_code=400, detail="Incorrect OTP code.")

    if AccountCrud.is_otp_expired(otp_record):
        raise HTTPException(status_code=400, detail="OTP code has expired.")

    AccountCrud.delete_otp(db, otp_record)

    token = Token.create_access_token(data={"sub": request.phone_number})
    return {"access_token": token, "token_type": "bearer"}       