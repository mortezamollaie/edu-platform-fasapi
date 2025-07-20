from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.learning import CreateLecture, UpdateLecture, RetrieveLecture
from app.models.learning import Course, Chapter, Lecture
from typing import List

router = APIRouter()

@router.get("/lectures", response_model=List[RetrieveLecture])
def get_lectures(db: Session = Depends(deps.get_db)):
    lectures = db.query(Lecture).all()
    return lectures

@router.get("/lectures/{slug}", response_model=RetrieveLecture)
def get_lecture(slug: str, db: Session = Depends(deps.get_db)):
    lecture = db.query(Lecture).filter(Lecture.slug == slug).first()
    if not lecture:
        raise HTTPException(status_code=404, detail="Lecture not found")
    return lecture

@router.post("/lectures", response_model=RetrieveLecture, status_code=status.HTTP_201_CREATED)
def create_lecture(payload: CreateLecture, db: Session = Depends(deps.get_db)):
    chapter = db.query(Chapter).filter(Chapter.slug == payload.chapter_slug).first()
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter with this slug not found.")
    
    payload_dict = payload.dict(exclude={"chapter_slug"})
    db_lecture = Lecture(**payload_dict)
    db_lecture.chapter = chapter

    db.add(db_lecture)
    db.commit()
    db.refresh(db_lecture)
    return db_lecture


@router.patch("/lectures/{slug}", response_model=RetrieveLecture, status_code=status.HTTP_200_OK)
def update_lecture(slug: str, payload: UpdateLecture, db: Session = Depends(deps.get_db)):
    lecture = db.query(Lecture).filter(Lecture.slug == slug).first()
    if not lecture:
        raise HTTPException(status_code=404, detail="Lecture not found")
    
    data = payload.dict(exclude_unset=True)

    chapter_slug = data.pop("chapter_slug", None)
    if chapter_slug:
        chapter = db.query(Chapter).filter(Chapter.slug == chapter_slug).first()
        if not chapter:
            raise HTTPException(status_code=404, detail="Chapter with this slug not found.")
        lecture.chapter = chapter

    for key, value in data.items():
        setattr(lecture, key, value)

    db.commit()
    db.refresh(lecture)
    return lecture


@router.delete("/lectures/{slug}", status_code=status.HTTP_204_NO_CONTENT)
def delete_lecture(slug: str, db: Session = Depends(deps.get_db)):
    lecture = db.query(Lecture).filter(Lecture.slug == slug).first()
    if not lecture:
        raise HTTPException(status_code=404, detail="Lecture not found")
    db.delete(lecture)
    db.commit()