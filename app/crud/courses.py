from sqlalchemy.orm import Session
from app.models.learning import Course
from app.schemas.learning import CreateCourse, UpdateCourse


def get_all_courses(db: Session):
    """
    Retrieve all courses from the database.
    
    Args:
        db (Session): SQLAlchemy database session.
    
    Returns:
        List[Course]: List of all course objects.
    """
    return db.query(Course).all()


def get_course_by_slug(db: Session, slug: str):
    """
    Retrieve a course by its slug.
    
    Args:
        db (Session): SQLAlchemy database session.
        slug (str): The slug of the course to retrieve.
    
    Returns:
        Course or None: The course object if found, None otherwise.
    """
    return db.query(Course).filter(Course.slug == slug).first()


def get_course_by_title(db: Session, title: str):
    """
    Retrieve a course by its title.
    
    Args:
        db (Session): SQLAlchemy database session.
        title (str): The title of the course to retrieve.
    
    Returns:
        Course or None: The course object if found, None otherwise.
    """
    return db.query(Course).filter(Course.title == title).first()


def create_course(db: Session, course_data: CreateCourse):
    """
    Create a new course in the database.
    
    Args:
        db (Session): SQLAlchemy database session.
        course_data (CreateCourse): Course data to create.
    
    Returns:
        Course: The created course object.
    """
    course = Course()
    for key, value in course_data.dict().items():
        setattr(course, key, value)

    db.add(course)
    db.commit()
    db.refresh(course)
    return course


def update_course(db: Session, slug: str, course_data: UpdateCourse):
    """
    Update a course's information.
    
    Args:
        db (Session): SQLAlchemy database session.
        slug (str): The slug of the course to update.
        course_data (UpdateCourse): Updated course data.
    
    Returns:
        Course or None: The updated course object if found, None otherwise.
    """
    course = get_course_by_slug(db, slug)
    if not course:
        return None
    
    for key, value in course_data.dict(exclude_unset=True).items():
        setattr(course, key, value)

    db.commit()
    db.refresh(course)
    return course


def delete_course(db: Session, slug: str):
    """
    Delete a course from the database.
    
    Args:
        db (Session): SQLAlchemy database session.
        slug (str): The slug of the course to delete.
    
    Returns:
        bool or None: True if deleted successfully, None if course not found.
    """
    course = get_course_by_slug(db, slug)
    if not course:
        return None
    
    db.delete(course)
    db.commit()
    return True


def get_course_chapters(db: Session, slug: str):
    """
    Get all chapters for a specific course.
    
    Args:
        db (Session): SQLAlchemy database session.
        slug (str): The slug of the course.
    
    Returns:
        List[Chapter] or None: List of chapters if course found, None otherwise.
    """
    course = get_course_by_slug(db, slug)
    if not course:
        return None
    return course.chapters
