from fastapi import Depends, APIRouter, status, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.schemas.account import SignUp, Register, Login, CreateUserRegisteredCourse, UserRegisteredCourseOut
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
def get_current_user_info(current_user: User = Depends(get_current_user)):
    return {
        "user_id": current_user.id,
        "email": current_user.email,
        "username": current_user.username,
        "is_registered": current_user.is_registered
    }


# UserRegisteredCourse APIs
@router.post("/register-course", status_code=status.HTTP_201_CREATED, response_model=UserRegisteredCourseOut, tags=["Course Registration"])
def register_course(
    payload: CreateUserRegisteredCourse,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(deps.get_db)
):
    """Register current user for a course"""
    registered_course = AccountCrud.create_user_registered_course(
        db, current_user.id, payload.course_id
    )
    
    if not registered_course:
        raise HTTPException(
            status_code=400, 
            detail="User is already registered for this course"
        )
    
    return registered_course


@router.get("/registered-courses", response_model=List[UserRegisteredCourseOut], tags=["Course Registration"])
def get_registered_courses(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(deps.get_db)
):
    """Get all courses registered by current user"""
    registered_courses = AccountCrud.get_user_registered_courses(db, current_user.id)
    return registered_courses


@router.get("/registered-courses/{course_id}", response_model=UserRegisteredCourseOut, tags=["Course Registration"])
def get_registered_course(
    course_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(deps.get_db)
):
    """Get specific registered course for current user"""
    registered_course = AccountCrud.get_user_registered_course(db, current_user.id, course_id)
    if not registered_course:
        raise HTTPException(
            status_code=404, 
            detail="Course registration not found"
        )
    
    return registered_course


@router.delete("/unregister-course/{course_id}", status_code=status.HTTP_200_OK, tags=["Course Registration"])
def unregister_course(
    course_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(deps.get_db)
):
    """Unregister current user from a course"""
    success = AccountCrud.delete_user_registered_course(db, current_user.id, course_id)
    if not success:
        raise HTTPException(
            status_code=404, 
            detail="Course registration not found"
        )
    
    return {"message": "Successfully unregistered from course"}
