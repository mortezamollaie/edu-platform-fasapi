from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.learning import CreateLecture, UpdateLecture, RetrieveLecture
import app.crud.lectures as lecturesCrud
import app.crud.account as AccountCrud
from typing import List
from app.dependencies import has_permission, get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/lectures", response_model=List[RetrieveLecture])
def get_lectures(db: Session = Depends(deps.get_db)):
    """Get list of all lectures"""
    return lecturesCrud.get_all_lectures(db)


@router.get("/lectures/{slug}", response_model=RetrieveLecture)
def get_lecture(slug: str, db: Session = Depends(deps.get_db), current_user: User = Depends(get_current_user)):
    """Retrieve a specific lecture by slug"""
    lecture = lecturesCrud.get_lecture_by_slug(db, slug)
    if not lecture:
        raise HTTPException(status_code=404, detail="Lecture not found")
    
    if lecture.is_free:
        return lecture
    
    course_id = lecture.chapter.course_id
    
    user_enrollment = AccountCrud.get_user_registered_course(db, current_user.id, course_id)
    if not user_enrollment:
        raise HTTPException(status_code=403, detail="You must be enrolled in this course to access this lecture")
    
    return lecture


@router.post("/lectures", response_model=RetrieveLecture, status_code=status.HTTP_201_CREATED)
def create_lecture(payload: CreateLecture, db: Session = Depends(deps.get_db), current_user: User = Depends(has_permission("manage_lectures"))):
    """Create a new lecture"""
    lecture = lecturesCrud.create_lecture(db, payload)
    if not lecture:
        raise HTTPException(status_code=404, detail="Chapter with this slug not found.")
    return lecture


@router.patch("/lectures/{slug}", response_model=RetrieveLecture, status_code=status.HTTP_200_OK)
def update_lecture(slug: str, payload: UpdateLecture, db: Session = Depends(deps.get_db), current_user: User = Depends(has_permission("manage_lectures"))):
    """Update a lecture's information"""
    lecture = lecturesCrud.update_lecture(db, slug, payload)
    if not lecture:
        raise HTTPException(status_code=404, detail="Lecture not found")
    elif lecture == "chapter_not_found":
        raise HTTPException(status_code=404, detail="Chapter with this slug not found.")
    return lecture


@router.delete("/lectures/{slug}", status_code=status.HTTP_204_NO_CONTENT)
def delete_lecture(slug: str, db: Session = Depends(deps.get_db), current_user: User = Depends(has_permission("manage_lectures"))):
    """Delete a lecture"""
    result = lecturesCrud.delete_lecture(db, slug)
    if not result:
        raise HTTPException(status_code=404, detail="Lecture not found")
    return {"message": "Lecture deleted successfully"}