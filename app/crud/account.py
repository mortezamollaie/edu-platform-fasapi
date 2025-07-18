from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.account import OtpCode


def get_otp_by_email(db: Session, email: str):
    """
    Retrieve an OTP record by email.
    """
    return db.query(OtpCode).filter(OtpCode.email == email).first()


def delete_otp(db: Session, otp: OtpCode):
    """
    Delete an OTP record from the database.

    Args:
        db (Session): SQLAlchemy database session.
        otp (OtpCode): The OTP record to delete.

    Returns:
        None
    """
    db.delete(otp)
    db.commit()


def create_otp(db: Session, email: str, code: str):
    """
    Create and store a new OTP record in the database using email.
    """
    otp = OtpCode(
        email=email,
        code=code,
        created_at=datetime.utcnow()
    )
    db.add(otp)
    db.commit()
    db.refresh(otp)
    return otp


def is_otp_expired(otp: OtpCode, minutes: int = 2):
    """
    Check if an OTP has expired based on its creation time.

    Args:
        otp (OtpCode): The OTP record to check.
        minutes (int, optional): Expiration window in minutes. Default is 2.

    Returns:
        bool: True if expired, False otherwise.
    """
    return (datetime.utcnow() - otp.created_at) > timedelta(minutes=minutes)
