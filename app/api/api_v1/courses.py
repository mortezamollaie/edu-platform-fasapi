from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.learning import CreateCourse, RetrieveCourse, UpdateCourse, RetrieveChapter
import app.crud.courses as coursesCrud
from typing import List

router = APIRouter()

@router.get("/courses", response_model=List[RetrieveCourse], status_code=status.HTTP_200_OK, tags=["Courses"])
def courses(db: Session = Depends(deps.get_db)):
    """Get list of all courses"""
    return coursesCrud.get_all_courses(db)


@router.post("/courses", response_model=RetrieveCourse, status_code=status.HTTP_201_CREATED, tags=["Courses"])
def create_course(payload: CreateCourse, db: Session = Depends(deps.get_db)):
    """Create a new course"""
    existing_course = coursesCrud.get_course_by_title(db, payload.title)
    if existing_course:
        raise HTTPException(status_code=400, detail="Course with this title already exists.")

    return coursesCrud.create_course(db, payload)


@router.get("/courses/{slug}", response_model=RetrieveCourse, status_code=status.HTTP_200_OK, tags=["Courses"])
def retrive_course(slug: str, db: Session = Depends(deps.get_db)):
    """Retrieve a specific course by slug"""
    course = coursesCrud.get_course_by_slug(db, slug)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course with this slug not found.")
    return course


@router.patch("/courses/{slug}")
def update_course(slug: str, payload: UpdateCourse, db: Session = Depends(deps.get_db)):
    """Update a course's information"""
    course = coursesCrud.update_course(db, slug, payload)
    if not course:
        raise HTTPException(status_code=404, detail="Course with this slug not found.")
    return course


@router.delete("/courses/{slug}")
def delete_course(slug: str, db: Session = Depends(deps.get_db)):
    """Delete a course"""
    result = coursesCrud.delete_course(db, slug)
    if not result:
        raise HTTPException(status_code=404, detail="Course with this slug not found.")
    return {"message": "Course deleted successfully"}


@router.get("/courses/{slug}/chapters", response_model=List[RetrieveChapter], status_code=status.HTTP_200_OK, tags=["Courses"])
def get_course_chapters(slug: str, db: Session = Depends(deps.get_db)):
    """Get all chapters for a specific course"""
    chapters = coursesCrud.get_course_chapters(db, slug)
    if chapters is None:
        raise HTTPException(status_code=404, detail="Course with this slug not found.")
    return chapters