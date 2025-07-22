from sqlalchemy.orm import Session
from app.models.learning import Chapter, Lecture
from app.schemas.learning import CreateLecture, UpdateLecture


def get_all_lectures(db: Session):
    """
    Retrieve all lectures from the database.
    
    Args:
        db (Session): SQLAlchemy database session.
    
    Returns:
        List[Lecture]: List of all lecture objects.
    """
    return db.query(Lecture).all()


def get_lecture_by_slug(db: Session, slug: str):
    """
    Retrieve a lecture by its slug.
    
    Args:
        db (Session): SQLAlchemy database session.
        slug (str): The slug of the lecture to retrieve.
    
    Returns:
        Lecture or None: The lecture object if found, None otherwise.
    """
    return db.query(Lecture).filter(Lecture.slug == slug).first()


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


def create_lecture(db: Session, lecture_data: CreateLecture):
    """
    Create a new lecture in the database.
    
    Args:
        db (Session): SQLAlchemy database session.
        lecture_data (CreateLecture): Lecture data to create.
    
    Returns:
        Lecture or None: The created lecture object if chapter found, None otherwise.
    """
    chapter = get_chapter_by_slug(db, lecture_data.chapter_slug)
    if not chapter:
        return None
    
    payload_dict = lecture_data.dict(exclude={"chapter_slug"})
    lecture = Lecture(**payload_dict)
    lecture.chapter = chapter

    db.add(lecture)
    db.commit()
    db.refresh(lecture)
    return lecture


def update_lecture(db: Session, slug: str, lecture_data: UpdateLecture):
    """
    Update a lecture's information.
    
    Args:
        db (Session): SQLAlchemy database session.
        slug (str): The slug of the lecture to update.
        lecture_data (UpdateLecture): Updated lecture data.
    
    Returns:
        Lecture or None: The updated lecture object if found, None otherwise.
    """
    lecture = get_lecture_by_slug(db, slug)
    if not lecture:
        return None

    data = lecture_data.dict(exclude_unset=True)
    chapter_slug = data.pop("chapter_slug", None)
    
    if chapter_slug:
        chapter = get_chapter_by_slug(db, chapter_slug)
        if not chapter:
            return "chapter_not_found"
        lecture.chapter = chapter

    for key, value in data.items():
        setattr(lecture, key, value)

    db.commit()
    db.refresh(lecture)
    return lecture


def delete_lecture(db: Session, slug: str):
    """
    Delete a lecture from the database.
    
    Args:
        db (Session): SQLAlchemy database session.
        slug (str): The slug of the lecture to delete.
    
    Returns:
        bool or None: True if deleted successfully, None if lecture not found.
    """
    lecture = get_lecture_by_slug(db, slug)
    if not lecture:
        return None
    
    db.delete(lecture)
    db.commit()
    return True