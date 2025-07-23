from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.user import User
from app.models.account import Role
from app.services.hash_password import Hash


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """
    Get a user by ID.
    """
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    Get a user by email.
    """
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """
    Get a user by username.
    """
    return db.query(User).filter(User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """
    Get all users with pagination.
    """
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, email: str, username: str = None, password: str = None, is_registered: bool = False) -> User:
    """
    Create a new user.
    """
    hashed_password = None
    if password:
        hashed_password = Hash().bcrypt(password)
    
    user = User(
        email=email,
        username=username,
        password=hashed_password,
        is_registered=is_registered
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, user_id: int, email: str = None, username: str = None, password: str = None, is_registered: bool = None) -> Optional[User]:
    """
    Update user information.
    """
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    
    if email is not None:
        user.email = email
    if username is not None:
        user.username = username
    if password is not None:
        user.password = Hash().bcrypt(password)
    if is_registered is not None:
        user.is_registered = is_registered
    
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int) -> bool:
    """
    Delete a user.
    """
    user = get_user_by_id(db, user_id)
    if not user:
        return False
    
    db.delete(user)
    db.commit()
    return True


def assign_roles_to_user(db: Session, user_id: int, role_ids: List[int]) -> Optional[User]:
    """
    Assign roles to a user.
    """
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    
    roles = db.query(Role).filter(Role.id.in_(role_ids)).all()
    user.roles = roles
    db.commit()
    db.refresh(user)
    return user


def add_roles_to_user(db: Session, user_id: int, role_ids: List[int]) -> Optional[User]:
    """
    Add new roles to existing user roles.
    """
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    
    # Get current role IDs
    current_role_ids = [role.id for role in user.roles]
    
    # Add new role IDs to existing ones (avoid duplicates)
    all_role_ids = list(set(current_role_ids + role_ids))
    
    # Get all roles and assign to user
    roles = db.query(Role).filter(Role.id.in_(all_role_ids)).all()
    user.roles = roles
    db.commit()
    db.refresh(user)
    return user


def remove_roles_from_user(db: Session, user_id: int, role_ids: List[int]) -> Optional[User]:
    """
    Remove specific roles from a user.
    """
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    
    # Get current role IDs
    current_role_ids = [role.id for role in user.roles]
    
    # Remove specified role IDs from current ones
    remaining_role_ids = [rid for rid in current_role_ids if rid not in role_ids]
    
    # Get remaining roles and assign to user
    roles = db.query(Role).filter(Role.id.in_(remaining_role_ids)).all()
    user.roles = roles
    db.commit()
    db.refresh(user)
    return user


def get_user_roles(db: Session, user_id: int) -> Optional[List[dict]]:
    """
    Get list of role names for a specific user.
    """
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    return [{"id": role.id, "name": role.name} for role in user.roles]


def search_users(db: Session, query: str, skip: int = 0, limit: int = 100) -> List[User]:
    """
    Search users by email or username.
    """
    return db.query(User).filter(
        (User.email.contains(query)) | (User.username.contains(query))
    ).offset(skip).limit(limit).all()


def get_users_count(db: Session) -> int:
    """
    Get total count of users.
    """
    return db.query(User).count()


def activate_user(db: Session, user_id: int) -> Optional[User]:
    """
    Activate a user (set is_registered to True).
    """
    return update_user(db, user_id, is_registered=True)


def deactivate_user(db: Session, user_id: int) -> Optional[User]:
    """
    Deactivate a user (set is_registered to False).
    """
    return update_user(db, user_id, is_registered=False)
