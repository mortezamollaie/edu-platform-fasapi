from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.account import OtpCode

def get_otp_by_phone(db: Session, phone_number: str):
    return db.query(OtpCode).filter(OtpCode.phone_number == phone_number).first()

def delete_otp(db: Session, otp: OtpCode):
    db.delete(otp)
    db.commit()

def create_otp(db: Session, phone_number: str, code: str):
    otp = OtpCode(
        phone_number=phone_number,
        code=code,
        created_at=datetime.utcnow()
    )
    db.add(otp)
    db.commit()
    db.refresh(otp)
    return otp

def is_otp_expired(otp: OtpCode, minutes: int = 2):
    return (datetime.utcnow() - otp.created_at) > timedelta(minutes=minutes)
