from pydantic import BaseModel, constr, validator
from typing import List

email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'

class SignUp(BaseModel):
    email: constr(pattern=email_pattern, max_length=255)
    username: constr(min_length=3, max_length=30)
    password: constr(min_length=8, max_length=16)
    password2: constr(min_length=8, max_length=16)

    @validator("password2")
    def passwords_match(cls, v, values):
        if "password" in values and v != values["password"]:
            raise ValueError("Passwords do not match")
        return v


class Register(BaseModel):
    email: constr(pattern=email_pattern)
    code: constr(min_length=6, max_length=6)


class Login(BaseModel):
    email: constr(pattern=email_pattern, max_length=255)
    password: constr(min_length=8, max_length=16)


class PermissionBase(BaseModel):
    name: str


class CreatePermission(PermissionBase):
    pass


class UpdatePermission(PermissionBase):
    pass


class PermissionOut(PermissionBase):
    id: int
    class Config:
        orm_mode = True


class RoleBase(BaseModel):
    name: str


class CreateRole(RoleBase):
    permission_ids: List[int] = []


class RoleOut(RoleBase):
    id: int
    permissions: List[PermissionOut]
    class Config:
        orm_mode = True