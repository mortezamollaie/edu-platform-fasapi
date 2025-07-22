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


def create_role(db: Session, role_data):
    """
    Create a new role in the database.
    
    Args:
        db (Session): SQLAlchemy database session.
        role_data: Role data containing name.
    
    Returns:
        Role: The created role object.
    """
    role = Role(name=role_data.name)
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


def get_role(db: Session, role_id: int):
    """
    Retrieve a role by its ID.
    
    Args:
        db (Session): SQLAlchemy database session.
        role_id (int): The ID of the role to retrieve.
    
    Returns:
        Role or None: The role object if found, None otherwise.
    """
    return db.query(Role).filter(Role.id == role_id).first()


def get_all_roles(db: Session):
    """
    Retrieve all roles from the database.
    
    Args:
        db (Session): SQLAlchemy database session.
    
    Returns:
        List[Role]: List of all role objects.
    """
    return db.query(Role).all()


def update_role(db: Session, role_id: int, data):
    """
    Update a role's name.
    
    Args:
        db (Session): SQLAlchemy database session.
        role_id (int): The ID of the role to update.
        data: Update data containing new name.
    
    Returns:
        Role or None: The updated role object if found, None otherwise.
    """
    role = get_role(db, role_id)
    if not role:
        return None
    role.name = data.name
    db.commit()
    db.refresh(role)
    return role


def delete_role(db: Session, role_id: int):
    """
    Delete a role from the database.
    
    Args:
        db (Session): SQLAlchemy database session.
        role_id (int): The ID of the role to delete.
    
    Returns:
        bool or None: True if deleted successfully, None if role not found.
    """
    role = get_role(db, role_id)
    if not role:
        return None
    db.delete(role)
    db.commit()
    return True


def assign_permissions_to_role(db: Session, role_id: int, permission_ids: list):
    """
    Replace all permissions for a role with new ones.
    
    Args:
        db (Session): SQLAlchemy database session.
        role_id (int): The ID of the role to update.
        permission_ids (list): List of permission IDs to assign.
    
    Returns:
        Role or None: The updated role object if found, None otherwise.
    """
    role = get_role(db, role_id)
    if not role:
        return None
    permissions = db.query(Permission).filter(Permission.id.in_(permission_ids)).all()
    role.permissions = permissions
    db.commit()
    db.refresh(role)
    return role


def add_permissions_to_role(db: Session, role_id: int, permission_ids: list):
    """
    Add new permissions to existing permissions of a role.
    
    Args:
        db (Session): SQLAlchemy database session.
        role_id (int): The ID of the role to update.
        permission_ids (list): List of permission IDs to add.
    
    Returns:
        Role or None: The updated role object if found, None otherwise.
    """
    role = get_role(db, role_id)
    if not role:
        return None
    
    # Get current permission IDs
    current_permission_ids = [perm.id for perm in role.permissions]
    
    # Add new permission IDs to existing ones (avoid duplicates)
    all_permission_ids = list(set(current_permission_ids + permission_ids))
    
    # Get all permissions and assign to role
    permissions = db.query(Permission).filter(Permission.id.in_(all_permission_ids)).all()
    role.permissions = permissions
    db.commit()
    db.refresh(role)
    return role


def remove_permissions_from_role(db: Session, role_id: int, permission_ids: list):
    """
    Remove specific permissions from a role.
    
    Args:
        db (Session): SQLAlchemy database session.
        role_id (int): The ID of the role to update.
        permission_ids (list): List of permission IDs to remove.
    
    Returns:
        Role or None: The updated role object if found, None otherwise.
    """
    role = get_role(db, role_id)
    if not role:
        return None
    
    # Get current permission IDs
    current_permission_ids = [perm.id for perm in role.permissions]
    
    # Remove specified permission IDs from current ones
    remaining_permission_ids = [pid for pid in current_permission_ids if pid not in permission_ids]
    
    # Get remaining permissions and assign to role
    permissions = db.query(Permission).filter(Permission.id.in_(remaining_permission_ids)).all()
    role.permissions = permissions
    db.commit()
    db.refresh(role)
    return role


def get_role_permissions(db: Session, role_id: int):
    """
    Get list of permission names for a specific role.
    
    Args:
        db (Session): SQLAlchemy database session.
        role_id (int): The ID of the role.
    
    Returns:
        List[dict] or None: List of permission names if role found, None otherwise.
    """
    role = get_role(db, role_id)
    if not role:
        return None
    return [{"name": perm.name} for perm in role.permissions]


def create_permission(db: Session, data):
    """
    Create a new permission in the database.
    
    Args:
        db (Session): SQLAlchemy database session.
        data: Permission data containing name.
    
    Returns:
        Permission: The created permission object.
    """
    perm = Permission(name=data.name)
    db.add(perm)
    db.commit()
    db.refresh(perm)
    return perm


def get_permission(db: Session, permission_id: int):
    """
    Retrieve a permission by its ID.
    
    Args:
        db (Session): SQLAlchemy database session.
        permission_id (int): The ID of the permission to retrieve.
    
    Returns:
        Permission or None: The permission object if found, None otherwise.
    """
    return db.query(Permission).filter(Permission.id == permission_id).first()


def get_all_permissions(db: Session):
    """
    Retrieve all permissions from the database.
    
    Args:
        db (Session): SQLAlchemy database session.
    
    Returns:
        List[Permission]: List of all permission objects.
    """
    return db.query(Permission).all()


def update_permission(db: Session, permission_id: int, data):
    """
    Update a permission's name.
    
    Args:
        db (Session): SQLAlchemy database session.
        permission_id (int): The ID of the permission to update.
        data: Update data containing new name.
    
    Returns:
        Permission or None: The updated permission object if found, None otherwise.
    """
    permission = get_permission(db, permission_id)
    if not permission:
        return None
    permission.name = data.name
    db.commit()
    db.refresh(permission)
    return permission


def delete_permission(db: Session, permission_id: int):
    """
    Delete a permission from the database.
    
    Args:
        db (Session): SQLAlchemy database session.
        permission_id (int): The ID of the permission to delete.
    
    Returns:
        bool or None: True if deleted successfully, None if permission not found.
    """
    permission = get_permission(db, permission_id)
    if not permission:
        return None
    db.delete(permission)
    db.commit()
    return True