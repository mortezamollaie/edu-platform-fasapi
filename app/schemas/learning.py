from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CreateCourse(BaseModel):
    title: str
    slug: str
    full_name: Optional[str] = None
    lecturer: Optional[str] = None
    language: Optional[str] = None
    is_free: Optional[bool] = False
    description: Optional[str] = None

class UpdateCourse(BaseModel):
    title: Optional[str] = None
    full_name: Optional[str] = None
    slug: Optional[str] = None
    lecturer: Optional[str] = None
    language: Optional[str] = None
    is_free: Optional[bool] = None
    description: Optional[str] = None

class RetriveCourse(BaseModel):
    id: int
    title: str
    slug: str
    full_name: Optional[str] = None
    lecturer: Optional[str] = None
    language: Optional[str] = None
    is_free: bool
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

