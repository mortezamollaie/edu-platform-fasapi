from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from app.db.base import Base
from datetime import datetime

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    full_name = Column(String, nullable=True)
    lecturer = Column(String, nullable=True)
    language = Column(String, nullable=True)
    is_free = Column(Boolean, default=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
