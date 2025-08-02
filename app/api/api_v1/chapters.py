from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.models.user import User
from app.schemas.learning import RetrieveChapter, CreateChapter, UpdateChapter, RetrieveLecture
import app.crud.chapters as chaptersCrud
from typing import List
from app.dependencies import has_permission

router = APIRouter()

@router.get("/chapters", response_model=List[RetrieveChapter], status_code=status.HTTP_200_OK, tags=["Chapters"])
def chapters(db: Session = Depends(deps.get_db)):
    """Get list of all chapters"""
    return chaptersCrud.get_all_chapters(db)


@router.post("/chapters", response_model=RetrieveChapter, status_code=status.HTTP_201_CREATED, tags=["Chapters"])
def create_chapter(payload: CreateChapter, db: Session = Depends(deps.get_db), current_user: User = Depends(has_permission("manage_chapters"))):
    """Create a new chapter"""
    chapter = chaptersCrud.create_chapter(db, payload)
    if not chapter:
        raise HTTPException(status_code=404, detail="Course with this slug not found.")
    return chapter


@router.get('/chapters/{slug}', response_model=RetrieveChapter, status_code=status.HTTP_200_OK, tags=["Chapters"])
def get_chapter(slug, db: Session = Depends(deps.get_db)):
    """Retrieve a specific chapter by slug"""
    chapter = chaptersCrud.get_chapter_by_slug(db, slug)
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter with this slug not found.")
    return chapter


@router.patch("/chapters/{slug}", response_model=RetrieveChapter, status_code=status.HTTP_200_OK, tags=["Chapters"])
def update_chapter(slug: str, payload: UpdateChapter, db: Session = Depends(deps.get_db), current_user: User = Depends(has_permission("manage_chapters"))):
    """Update a chapter's information"""
    chapter = chaptersCrud.update_chapter(db, slug, payload)
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter with this slug not found.")
    elif chapter == "course_not_found":
        raise HTTPException(status_code=404, detail="Course with this slug not found.")
    return chapter


@router.delete("/chapters/{slug}", status_code=status.HTTP_200_OK, tags=["Chapters"])
def delete_chapter(slug: str, db: Session = Depends(deps.get_db), current_user: User = Depends(has_permission("manage_chapters"))):
    """Delete a chapter"""
    result = chaptersCrud.delete_chapter(db, slug)
    if not result:
        raise HTTPException(status_code=404, detail="Chapter with this slug not found.")
    return {"message": "Chapter deleted successfully"}


@router.get("/chapters/{slug}/lectures", response_model=List[RetrieveLecture], status_code=status.HTTP_200_OK, tags=["Lectures"])
def get_chapter_lectures(slug: str, db: Session = Depends(deps.get_db)):
    """Get all lectures for a specific chapter"""
    lectures = chaptersCrud.get_chapter_lectures(db, slug)
    if lectures is None:
        raise HTTPException(status_code=404, detail="Chapter with this slug not found.")
    return lectures