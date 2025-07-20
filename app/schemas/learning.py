from pydantic import BaseModel
from typing import Optional
import datetime

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

class RetrieveCourse(BaseModel):
    id: int
    title: str
    slug: str
    full_name: Optional[str] = None
    lecturer: Optional[str] = None
    language: Optional[str] = None
    is_free: bool
    description: Optional[str] = None
    updated_at: datetime.datetime

    class Config:
        orm_mode = True


class CreateChapter(BaseModel):
    title: str
    slug: str
    is_free: Optional[bool] = False
    course_slug: str   


class UpdateChapter(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    is_free: Optional[bool] = False
    course_slug: Optional[str] = None


class RetrieveChapter(BaseModel):
    id: int
    title: str
    slug: str
    is_free: bool

    class Config:
        orm_mode = True


class CreateLecture(BaseModel):
    title: str
    slug: str
    time: datetime.time
    is_free: Optional[bool] = False
    video_url: Optional[str] = None
    drive_url: Optional[str] = None
    youtube_url: Optional[str] = None
    chapter_slug: str


class UpdateLecture(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    time: Optional[datetime.time] = None
    is_free: Optional[bool] = None
    video_url: Optional[str] = None
    drive_url: Optional[str] = None
    youtube_url: Optional[str] = None
    chapter_slug: Optional[str] = None


class RetrieveLecture(BaseModel):
    id: int
    title: str
    slug: str
    time: datetime.time
    is_free: bool
    video_url: Optional[str] = None
    drive_url: Optional[str] = None
    youtube_url: Optional[str] = None

    class Config:
        orm_mode = True


