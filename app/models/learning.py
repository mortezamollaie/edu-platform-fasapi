from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from app.db.base import Base
from datetime import datetime
from sqlalchemy.orm import relationship


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    full_name = Column(String, nullable=True)
    slug = Column(String)
    lecturer = Column(String, nullable=True)
    language = Column(String, nullable=True)
    is_free = Column(Boolean, default=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    chapters = relationship("Chapter", back_populates="course", cascade="all, delete-orphan")


class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    slug = Column(String)
    is_free = Column(Boolean, default=False)
    course_id = Column(Integer, ForeignKey("courses.id"))
    course = relationship("Course", back_populates="chapters")


