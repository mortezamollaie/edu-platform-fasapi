from pydantic import BaseModel, EmailStr, constr, validator
from typing import List, Optional
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    username: Optional[str] = None


class UserCreate(UserBase):
    password: constr(min_length=8, max_length=50)
    password2: constr(min_length=8, max_length=50)
    
    @validator("password2")
    def passwords_match(cls, v, values):
        if "password" in values and v != values["password"]:
            raise ValueError("Passwords do not match")
        return v


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[constr(min_length=8, max_length=50)] = None
    is_registered: Optional[bool] = None


class UserPasswordUpdate(BaseModel):
    current_password: constr(min_length=8, max_length=50)
    new_password: constr(min_length=8, max_length=50)
    confirm_password: constr(min_length=8, max_length=50)
    
    @validator("confirm_password")
    def passwords_match(cls, v, values):
        if "new_password" in values and v != values["new_password"]:
            raise ValueError("New passwords do not match")
        return v


class RoleBase(BaseModel):
    id: int
    name: str


class UserOut(UserBase):
    id: int
    is_registered: bool
    roles: Optional[List[RoleBase]] = []
    
    class Config:
        orm_mode = True


class UserListOut(BaseModel):
    id: int
    email: str
    username: Optional[str] = None
    is_registered: bool
    
    class Config:
        orm_mode = True


class UserDetailOut(UserOut):
    roles: List[RoleBase] = []
    
    class Config:
        orm_mode = True


class UserRoleAssignment(BaseModel):
    role_ids: List[int]


class UserSearch(BaseModel):
    query: str
    skip: Optional[int] = 0
    limit: Optional[int] = 100


class UsersResponse(BaseModel):
    users: List[UserListOut]
    total: int
    skip: int
    limit: int


class UserActivation(BaseModel):
    is_active: bool
