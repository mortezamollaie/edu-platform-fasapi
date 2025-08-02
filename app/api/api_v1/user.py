from fastapi import Depends, APIRouter, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.api import deps
from app.models.user import User
from app.crud import user as UserCrud
from app.schemas.user import (
    UserCreate, UserUpdate, UserOut, UserListOut, UserDetailOut,
    UserPasswordUpdate, UserRoleAssignment, UsersResponse, UserActivation
)
from app.dependencies import get_current_user, has_permission
from app.services.hash_password import Hash

router = APIRouter()

@router.get("/users", response_model=UsersResponse, tags=["Users"])
def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    current_user: User = Depends(has_permission("view_users")),
    db: Session = Depends(deps.get_db)
):
    """Get all users with pagination and search"""
    if search:
        users = UserCrud.search_users(db, search, skip, limit)
    else:
        users = UserCrud.get_users(db, skip, limit)
    
    total = UserCrud.get_users_count(db)
    
    # Convert User objects to UserListOut format
    users_data = [
        UserListOut(
            id=user.id,
            email=user.email,
            username=user.username,
            is_registered=user.is_registered
        ) for user in users
    ]
    
    return UsersResponse(
        users=users_data,
        total=total,
        skip=skip,
        limit=limit
    )


@router.get("/users/{user_id}", response_model=UserDetailOut, tags=["Users"])
def get_user(
    user_id: int,
    current_user: User = Depends(has_permission("view_users")),
    db: Session = Depends(deps.get_db)
):
    """Get a specific user by ID"""
    user = UserCrud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED, tags=["Users"])
def create_user(
    user_data: UserCreate,
    current_user: User = Depends(has_permission("create_users")),
    db: Session = Depends(deps.get_db)
):
    """Create a new user"""
    # Check if email already exists
    existing_user = UserCrud.get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Check if username already exists (if provided)
    if user_data.username:
        existing_username = UserCrud.get_user_by_username(db, user_data.username)
        if existing_username:
            raise HTTPException(status_code=400, detail="Username already taken")
    
    user = UserCrud.create_user(
        db=db,
        email=user_data.email,
        username=user_data.username,
        password=user_data.password,
        is_registered=True
    )
    return user


@router.put("/users/{user_id}", response_model=UserOut, tags=["Users"])
def update_user(
    user_id: int,
    user_data: UserUpdate,
    current_user: User = Depends(has_permission("edit_users")),
    db: Session = Depends(deps.get_db)
):
    """Update a user"""
    # Check if user exists
    existing_user = UserCrud.get_user_by_id(db, user_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if email is being changed and if it's already taken
    if user_data.email and user_data.email != existing_user.email:
        email_user = UserCrud.get_user_by_email(db, user_data.email)
        if email_user:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    # Check if username is being changed and if it's already taken
    if user_data.username and user_data.username != existing_user.username:
        username_user = UserCrud.get_user_by_username(db, user_data.username)
        if username_user:
            raise HTTPException(status_code=400, detail="Username already taken")
    
    updated_user = UserCrud.update_user(
        db=db,
        user_id=user_id,
        email=user_data.email,
        username=user_data.username,
        password=user_data.password,
        is_registered=user_data.is_registered
    )
    return updated_user


@router.delete("/users/{user_id}", status_code=status.HTTP_200_OK, tags=["Users"])
def delete_user(
    user_id: int,
    current_user: User = Depends(has_permission("delete_users")),
    db: Session = Depends(deps.get_db)
):
    """Delete a user"""
    # Prevent self-deletion
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot delete your own account")
    
    success = UserCrud.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"message": "User deleted successfully"}


@router.put("/users/{user_id}/roles", response_model=UserOut, tags=["Users", "Roles"])
def assign_roles_to_user(
    user_id: int,
    role_data: UserRoleAssignment,
    current_user: User = Depends(has_permission("manage_user_roles")),
    db: Session = Depends(deps.get_db)
):
    """Assign roles to a user (replaces existing roles)"""
    user = UserCrud.assign_roles_to_user(db, user_id, role_data.role_ids)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/users/{user_id}/roles", response_model=UserOut, tags=["Users", "Roles"])
def add_roles_to_user(
    user_id: int,
    role_data: UserRoleAssignment,
    current_user: User = Depends(has_permission("manage_user_roles")),
    db: Session = Depends(deps.get_db)
):
    """Add roles to a user (keeps existing roles)"""
    user = UserCrud.add_roles_to_user(db, user_id, role_data.role_ids)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/users/{user_id}/roles", response_model=UserOut, tags=["Users", "Roles"])
def remove_roles_from_user(
    user_id: int,
    role_data: UserRoleAssignment,
    current_user: User = Depends(has_permission("manage_user_roles")),
    db: Session = Depends(deps.get_db)
):
    """Remove specific roles from a user"""
    user = UserCrud.remove_roles_from_user(db, user_id, role_data.role_ids)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/users/{user_id}/roles", tags=["Users", "Roles"])
def get_user_roles(
    user_id: int,
    current_user: User = Depends(has_permission("manage_user_roles")),
    db: Session = Depends(deps.get_db)
):
    """Get roles assigned to a user"""
    roles = UserCrud.get_user_roles(db, user_id)
    if roles is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user_id": user_id, "roles": roles}


@router.put("/users/{user_id}/password", tags=["Users"])
def update_user_password(
    user_id: int,
    password_data: UserPasswordUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(deps.get_db)
):
    """Update user password (only own password or admin)"""
    # Check if user is updating their own password or is admin
    if user_id != current_user.id:
        # Check if current user has permission to edit other users
        for role in current_user.roles:
            for perm in role.permissions:
                if perm.name == "edit_users":
                    break
            else:
                continue
            break
        else:
            raise HTTPException(
                status_code=403, 
                detail="You can only update your own password"
            )
    
    user = UserCrud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify current password
    if not Hash().verify(password_data.current_password, user.password):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    
    # Update password
    updated_user = UserCrud.update_user(db, user_id, password=password_data.new_password)
    return {"message": "Password updated successfully"}


@router.put("/users/{user_id}/activate", response_model=UserOut, tags=["Users"])
def activate_user(
    user_id: int,
    current_user: User = Depends(has_permission("manage_users")),
    db: Session = Depends(deps.get_db)
):
    """Activate a user"""
    user = UserCrud.activate_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/users/{user_id}/deactivate", response_model=UserOut, tags=["Users"])
def deactivate_user(
    user_id: int,
    current_user: User = Depends(has_permission("manage_users")),
    db: Session = Depends(deps.get_db)
):
    """Deactivate a user"""
    # Prevent self-deactivation
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot deactivate your own account")
    
    user = UserCrud.deactivate_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Current user endpoints
@router.get("/me", response_model=UserDetailOut, tags=["Current User"])
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Get current user profile"""
    return current_user


@router.put("/me", response_model=UserOut, tags=["Current User"])
def update_current_user_profile(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(deps.get_db)
):
    """Update current user profile"""
    # Check if email is being changed and if it's already taken
    if user_data.email and user_data.email != current_user.email:
        email_user = UserCrud.get_user_by_email(db, user_data.email)
        if email_user:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    # Check if username is being changed and if it's already taken
    if user_data.username and user_data.username != current_user.username:
        username_user = UserCrud.get_user_by_username(db, user_data.username)
        if username_user:
            raise HTTPException(status_code=400, detail="Username already taken")
    
    # Don't allow changing is_registered through this endpoint
    user_data.is_registered = None
    
    updated_user = UserCrud.update_user(
        db=db,
        user_id=current_user.id,
        email=user_data.email,
        username=user_data.username,
        password=user_data.password
    )
    return updated_user