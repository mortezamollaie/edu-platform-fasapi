from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.account import OtpCode
from app.models.account import Role, Permission
from app.schemas.account import CreatePermission, CreateRole


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


def create_role(db: Session, role_data: CreateRole):
    role = Role(name=role_data.name)
    if role_data.permission_ids:
        permissions = db.query(Permission).filter(Permission.id.in_(role_data.permission_ids)).all()
        role.permissions = permissions
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


def get_role(db: Session, role_id: int):
    return db.query(Role).filter(Role.id == role_id).first()


def get_all_roles(db: Session):
    return db.query(Role).all()


def update_role(db: Session, role_id: int, data: CreateRole):
    role = get_role(db, role_id)
    if not role:
        return None
    role.name = data.name
    role.permissions = db.query(Permission).filter(Permission.id.in_(data.permission_ids)).all()
    db.commit()
    db.refresh(role)
    return role


def delete_role(db: Session, role_id: int):
    role = get_role(db, role_id)
    if not role:
        return None
    db.delete(role)
    db.commit()
    return True


def create_permission(db: Session, data: CreatePermission):
    perm = Permission(name=data.name)
    db.add(perm)
    db.commit()
    db.refresh(perm)
    return perm


def get_all_permissions(db: Session):
    return db.query(Permission).all()