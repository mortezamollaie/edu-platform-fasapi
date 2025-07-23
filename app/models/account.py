from sqlalchemy import Column, Integer, String, DateTime, Table, ForeignKey
from app.db.base_class import Base
from sqlalchemy.orm import relationship
from datetime import datetime

role_permission = Table(
    'role_permission', Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id')),
    Column('permission_id', Integer, ForeignKey('permissions.id'))
)


user_role = Table(
    'user_role', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('role_id', Integer, ForeignKey('roles.id')),
    extend_existing=True
) 


user_registered_course = Table(
    'user_registered_course', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('course_id', Integer, ForeignKey('courses.id')),
    extend_existing=True
)


class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    permissions = relationship('Permission', secondary=role_permission, back_populates='roles')


class Permission(Base):
    __tablename__ = 'permissions'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    roles = relationship('Role', secondary=role_permission, back_populates='permissions')


class UserRegisteredCourse(Base):
    __tablename__ = "user_registered_courses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    registered_at = Column(DateTime, default=datetime.utcnow)


class OtpCode(Base):
    __tablename__ = "otp_codes"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), nullable=False, index=True)
    code = Column(String(6), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
