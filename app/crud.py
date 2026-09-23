
from sqlalchemy.orm import Session
from . import models, schemas


def create_student(db: Session, student: schemas.StudentCreate):
    db_student = models.Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def get_student(db: Session, student_id: int):
    return (
        db.query(models.Student)
        .filter(models.Student.id == student_id)
        .first()
    )


def get_students(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Student)
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_student(
    db: Session,
    student_id: int,
    student_data: schemas.StudentUpdate
):
    student = get_student(db, student_id)

    if not student:
        return None

    update_data = student_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(student, key, value)

    db.commit()
    db.refresh(student)

    return student


def delete_student(db: Session, student_id: int):
    student = get_student(db, student_id)

    if not student:
        return None

    db.delete(student)
    db.commit()

    return student
