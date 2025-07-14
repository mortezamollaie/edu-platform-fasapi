from pydantic import BaseModel

class SignUp(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str