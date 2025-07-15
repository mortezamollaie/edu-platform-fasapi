from pydantic import BaseModel, constr, Field

class SignUp(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str


class SignUpResponse(SignUp):
    first_name: str
    last_name: str
    email: str

    class Config():
        orm_mode = True    


class SendOtp(BaseModel):
    first_name: constr(max_length=50)
    last_name: constr(max_length=50)
    phone_number: str = Field(..., pattern=r'^09\d{9}$')


class VerifyOtp(BaseModel):
    phone_number: str = Field(..., pattern=r'^09\d{9}$')
    code: constr(min_length=6, max_length=6)
