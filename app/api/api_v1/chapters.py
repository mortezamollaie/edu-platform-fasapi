from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.learning import RetrieveChapter, CreateChapter, UpdateChapter
from app.models.learning import Course, Chapter
from typing import List

router = APIRouter()

@router.get("/chapters", response_model=List[RetrieveChapter], status_code=status.HTTP_200_OK, tags=["Chapters"])
def chapters(db: Session = Depends(deps.get_db)):
    chapters = db.query(Chapter).all()
    return chapters


@router.post("/chapters", response_model=RetrieveChapter, status_code=status.HTTP_201_CREATED, tags=["Chapters"])
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


@router.get('/chapters/{slug}', response_model=RetrieveChapter, status_code=status.HTTP_200_OK, tags=["Chapters"])
def get_chapter(slug, db: Session = Depends(deps.get_db)):
    chapter = db.query(Chapter).filter(Chapter.slug == slug).first()
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter with this slug not found.")
    return chapter


@router.patch("/chapters/{slug}", response_model=RetrieveChapter, status_code=status.HTTP_200_OK, tags=["Chapters"])
def update_chapter(slug: str, payload: UpdateChapter, db: Session = Depends(deps.get_db)):
    chapter = db.query(Chapter).filter(Chapter.slug == slug).first()
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter with this slug not found.")

    data = payload.dict(exclude_unset=True)

    course_slug = data.pop("course_slug", None)
    if course_slug:
        course = db.query(Course).filter(Course.slug == course_slug).first()
        if not course:
            raise HTTPException(status_code=404, detail="Course with this slug not found.")
        chapter.course = course

    for field, value in data.items():
        setattr(chapter, field, value)

    db.commit()
    db.refresh(chapter)
    return chapter


@router.delete("/chapters/{slug}", status_code=status.HTTP_200_OK, tags=["Chapters"])
def delete_chapter(slug: str, db: Session = Depends(deps.get_db)):
    chapter = db.query(Chapter).filter(Chapter.slug == slug).first()
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter with this slug not found.")

    db.delete(chapter)
    db.commit()
    return
