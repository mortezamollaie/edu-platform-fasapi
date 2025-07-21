from sqlalchemy import Column, Integer, String, Boolean
from app.db.base_class import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, nullable=True)
    password = Column(String, nullable=True)
    is_registered = Column(Boolean, default=False)