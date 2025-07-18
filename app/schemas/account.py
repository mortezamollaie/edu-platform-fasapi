from pydantic import BaseModel, constr, validator

email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'

class SignUp(BaseModel):
    email: constr(pattern=email_pattern)
    username: constr(min_length=3, max_length=30)
    password: constr(min_length=8, max_length=128)
    password2: constr(min_length=8, max_length=128)

    @validator("password2")
    def passwords_match(cls, v, values):
        if "password" in values and v != values["password"]:
            raise ValueError("Passwords do not match")
        return v


class Register(BaseModel):
    email: constr(pattern=email_pattern)
    code: constr(min_length=6, max_length=6)
