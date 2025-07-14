from pydantic import BaseModel

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