from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.learning import RetriveChapter, CreateChapter
from app.models.learning import Course, Chapter
from typing import List

router = APIRouter()

@router.get("/chapters", response_model=List[RetriveChapter], status_code=status.HTTP_200_OK, tags=["Chapters"])
def chapters(db: Session = Depends(deps.get_db)):
    chapters = db.query(Chapter).all()
    return chapters


@router.post("/chapters", response_model=RetriveChapter, status_code=status.HTTP_201_CREATED, tags=["Chapters"])
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


