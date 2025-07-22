from sqlalchemy.orm import Session
from app.models.learning import Course, Chapter
from app.schemas.learning import CreateChapter, UpdateChapter


def get_all_chapters(db: Session):
    """
    Retrieve all chapters from the database.
    
    Args:
        db (Session): SQLAlchemy database session.
    
    Returns:
        List[Chapter]: List of all chapter objects.
    """
    return db.query(Chapter).all()


def get_chapter_by_slug(db: Session, slug: str):
    """
    Retrieve a chapter by its slug.
    
    Args:
        db (Session): SQLAlchemy database session.
        slug (str): The slug of the chapter to retrieve.
    
    Returns:
        Chapter or None: The chapter object if found, None otherwise.
    """
    return db.query(Chapter).filter(Chapter.slug == slug).first()


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


def create_chapter(db: Session, chapter_data: CreateChapter):
    """
    Create a new chapter in the database.
    
    Args:
        db (Session): SQLAlchemy database session.
        chapter_data (CreateChapter): Chapter data to create.
    
    Returns:
        Chapter or None: The created chapter object if course found, None otherwise.
    """
    course = get_course_by_slug(db, chapter_data.course_slug)
    if not course:
        return None
    
    payload_dict = chapter_data.dict(exclude={"course_slug"})
    chapter = Chapter(**payload_dict)
    chapter.course_id = course.id

    db.add(chapter)
    db.commit()
    db.refresh(chapter)
    return chapter


def update_chapter(db: Session, slug: str, chapter_data: UpdateChapter):
    """
    Update a chapter's information.
    
    Args:
        db (Session): SQLAlchemy database session.
        slug (str): The slug of the chapter to update.
        chapter_data (UpdateChapter): Updated chapter data.
    
    Returns:
        Chapter or None: The updated chapter object if found, None otherwise.
    """
    chapter = get_chapter_by_slug(db, slug)
    if not chapter:
        return None

    data = chapter_data.dict(exclude_unset=True)
    course_slug = data.pop("course_slug", None)
    
    if course_slug:
        course = get_course_by_slug(db, course_slug)
        if not course:
            return "course_not_found"
        chapter.course = course

    for field, value in data.items():
        setattr(chapter, field, value)

    db.commit()
    db.refresh(chapter)
    return chapter


def delete_chapter(db: Session, slug: str):
    """
    Delete a chapter from the database.
    
    Args:
        db (Session): SQLAlchemy database session.
        slug (str): The slug of the chapter to delete.
    
    Returns:
        bool or None: True if deleted successfully, None if chapter not found.
    """
    chapter = get_chapter_by_slug(db, slug)
    if not chapter:
        return None
    
    db.delete(chapter)
    db.commit()
    return True


def get_chapter_lectures(db: Session, slug: str):
    """
    Get all lectures for a specific chapter.
    
    Args:
        db (Session): SQLAlchemy database session.
        slug (str): The slug of the chapter.
    
    Returns:
        List[Lecture] or None: List of lectures if chapter found, None otherwise.
    """
    chapter = get_chapter_by_slug(db, slug)
    if not chapter:
        return None
    return chapter.lectures
