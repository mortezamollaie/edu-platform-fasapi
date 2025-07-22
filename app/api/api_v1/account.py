from fastapi import Depends, APIRouter, status, HTTPException, Request
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.account import SignUp, Register, Login
from app.services import token_management_service as Token
from app.services import hash_password
from app.crud import account as AccountCrud
from app.models.user import User
from app.dependencies import get_current_user
import random

router = APIRouter()

@router.post("/signup", status_code=status.HTTP_200_OK, tags=["Accounts"])
def signup(request: Request, payload: SignUp, db: Session = Depends(deps.get_db)):
    existing_user = db.query(User).filter(User.email == payload.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered.")

    code = str(random.randint(100000, 999999))
    print(f"OTP code for {payload.email}: {code}")

    existing_otp = AccountCrud.get_otp_by_email(db, payload.email)
    if existing_otp:
        AccountCrud.delete_otp(db, existing_otp)
    AccountCrud.create_otp(db, payload.email, code)

    request.session['signup_data'] = {
        "email": payload.email,
        "username": payload.username,
        "password": payload.password
    }

    return {"message": "OTP sent successfully."}


@router.post("/register", status_code=200, tags=["Accounts"])
def register(request: Request, payload: Register, db: Session = Depends(deps.get_db)):
    signup_data = request.session.get("signup_data")
    if not signup_data or signup_data.get("email") != payload.email:
        raise HTTPException(status_code=400, detail="Signup session data not found or mismatch")

    otp_record = AccountCrud.get_otp_by_email(db, payload.email)
    if not otp_record:
        raise HTTPException(status_code=404, detail="OTP code not found.")
    if otp_record.code != payload.code:
        raise HTTPException(status_code=400, detail="Incorrect OTP code.")
    if AccountCrud.is_otp_expired(otp_record):
        raise HTTPException(status_code=400, detail="OTP code has expired.")

    AccountCrud.delete_otp(db, otp_record)

    signup_data['password'] = hash_password.Hash().bcrypt(password=signup_data['password'])

    user = User(
        email=signup_data["email"],
        username=signup_data["username"],
        password=signup_data["password"],
        is_registered=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    request.session.pop("signup_data", None)

    token = Token.create_access_token(data={"sub": user.email})

    return {"message": "User registered successfully.", "user_id": user.id, "token": token}


@router.post("/login", status_code=200, tags=["Accounts"])
def login(payload: Login, db: Session = Depends(deps.get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User with this email not found.")

    if not hash_password.Hash().verify(payload.password, user.password):
        return HTTPException(status_code=400, detail="Password was incorrect.")
    
    token = Token.create_access_token(data={"sub": user.email})

    return {"message": "User logged in successfully.", "user_id": user.id, "token": token}


@router.get("/current-user")
def get_current_user(current_user=Depends(get_current_user)):
    return {"message": f"Hello user {current_user['user_id']}"}