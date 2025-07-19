from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.learning import CreateCourse, RetriveCourse
from app.models.learning import Course

router = APIRouter()

@router.get("/courses", status_code=status.HTTP_200_OK, tags=["Learning"])
def courses():
    pass

@router.get("/")


# TODO : implement permission for creating with admin
@router.post("/courses", response_model=RetriveCourse, status_code=status.HTTP_201_CREATED, tags=["Learning"])
def create_course(payload: CreateCourse, db: Session = Depends(deps.get_db)):
    existing_course = db.query(Course).filter(Course.title == payload.title).first()
    if existing_course:
        raise HTTPException(status_code=400, detail="Course with this title already exists.")
    
    course = Course(
        title = payload.title,
        full_name = payload.full_name,
        lecturer = payload.lecturer,
        language = payload.language,
        is_free = payload.is_free,
        description = payload.description
    )
    db.add(course)
    db.commit()
    db.refresh(course)
    return course