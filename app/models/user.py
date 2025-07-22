from sqlalchemy import Column, Integer, String, Boolean, Table, ForeignKey
from app.db.base_class import Base
from sqlalchemy.orm import relationship

user_role = Table(
    'user_role', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('role_id', Integer, ForeignKey('roles.id')),
    extend_existing=True
) 

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, nullable=True)
    password = Column(String, nullable=True)
    is_registered = Column(Boolean, default=False)
    roles = relationship('Role', secondary=user_role)