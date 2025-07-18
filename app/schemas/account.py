from pydantic import BaseModel, constr, EmailStr

class SendOtp(BaseModel):
    email: constr()


class VerifyOtp(BaseModel):
    email: constr()
    code: constr(min_length=6, max_length=6)
