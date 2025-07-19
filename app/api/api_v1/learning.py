from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.learning import CreateCourse, RetriveCourse
from app.models.learning import Course
from typing import List

router = APIRouter()

@router.get("/courses", response_model=List[RetriveCourse], status_code=status.HTTP_200_OK, tags=["Learning"])
def courses(db: Session = Depends(deps.get_db)):
    courses = db.query(Course).all()
    return courses

# TODO : implement permission for creating with admin
@router.post("/courses", response_model=RetriveCourse, status_code=status.HTTP_201_CREATED, tags=["Learning"])
def create_course(payload: CreateCourse, db: Session = Depends(deps.get_db)):
    existing_course = db.query(Course).filter(Course.title == payload.title).first()
    if existing_course:
        raise HTTPException(status_code=400, detail="Course with this title already exists.")
    
    course = Course(
        title = payload.title,
        full_name = payload.full_name,
        slug=payload.slug,
        lecturer = payload.lecturer,
        language = payload.language,
        is_free = payload.is_free,
        description = payload.description
    )
    db.add(course)
    db.commit()
    db.refresh(course)
    return course

@router.get("/courses/{slug}", response_model=RetriveCourse, status_code=status.HTTP_200_OK, tags=["Learning"])
def retrive_course(slug: str, db: Session = Depends(deps.get_db)):
    course = db.query(Course).filter(Course.slug == slug).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course with this id not found.")
    return course