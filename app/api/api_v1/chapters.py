from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.learning import ReadChapter, CreateChapter
from app.models.learning import Course, Chapter
from typing import List

router = APIRouter()

@router.post("/chapters", response_model=ReadChapter, status_code=status.HTTP_201_CREATED, tags=["Learning"])
def create_chapter(payload: CreateChapter, db: Session = Depends(deps.get_db)):
    course = db.query(Course).filter(Course.slug == payload.course_slug).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course with this slug not found.")

    payload_dict = payload.dict(exclude={"course_slug"})

    chapter = Chapter(**payload_dict)
    chapter.course_id = course.id

    db.add(chapter)
    db.commit()
    db.refresh(chapter)
    return chapter


