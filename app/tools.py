
from typing import Optional

from langchain_core.tools import tool

from .database import SessionLocal
from .models import Student


@tool
def get_student(student_id: int) -> dict:
    """
    Get complete information about a student using the student's ID.
    """

    db = SessionLocal()

    try:
        student = (
            db.query(Student)
            .filter(Student.id == student_id)
            .first()
        )

        if not student:
            return {
                "success": False,
                "message": f"Student with ID {student_id} was not found."
            }

        return {
            "success": True,
            "student": {
                "id": student.id,
                "name": student.name,
                "age": student.age,
                "gender": student.gender,
                "department": student.department,
                "email": student.email,
                "phone": student.phone,
                "gpa": student.gpa
            }
        }

    finally:
        db.close()


@tool
def get_all_students() -> list:
    """
    Get information about all students in the database.
    """

    db = SessionLocal()

    try:
        students = db.query(Student).all()

        return [
            {
                "id": student.id,
                "name": student.name,
                "department": student.department,
                "gpa": student.gpa
            }
            for student in students
        ]

    finally:
        db.close()


@tool
def find_students_by_department(department: str) -> list:
    """
    Find all students belonging to a particular department.
    """

    db = SessionLocal()

    try:
        students = (
            db.query(Student)
            .filter(Student.department.ilike(department))
            .all()
        )

        return [
            {
                "id": student.id,
                "name": student.name,
                "department": student.department,
                "gpa": student.gpa,
                "email": student.email
            }
            for student in students
        ]

    finally:
        db.close()


@tool
def find_students_by_min_gpa(min_gpa: float) -> list:
    """
    Find all students whose GPA is greater than or equal to the given GPA.
    """

    db = SessionLocal()

    try:
        students = (
            db.query(Student)
            .filter(Student.gpa >= min_gpa)
            .order_by(Student.gpa.desc())
            .all()
        )

        return [
            {
                "id": student.id,
                "name": student.name,
                "department": student.department,
                "gpa": student.gpa
            }
            for student in students
        ]

    finally:
        db.close()


@tool
def update_student_gpa(student_id: int, new_gpa: float) -> dict:
    """
    Update the GPA of a student using the student's ID.
    """

    db = SessionLocal()

    try:
        student = (
            db.query(Student)
            .filter(Student.id == student_id)
            .first()
        )

        if not student:
            return {
                "success": False,
                "message": f"Student with ID {student_id} was not found."
            }

        old_gpa = student.gpa
        student.gpa = new_gpa

        db.commit()
        db.refresh(student)

        return {
            "success": True,
            "message": f"GPA updated successfully for student {student_id}.",
            "student_id": student_id,
            "old_gpa": old_gpa,
            "new_gpa": student.gpa
        }

    finally:
        db.close()


@tool
def delete_student(student_id: int) -> dict:
    """
    Delete a student from the database using the student's ID.
    """

    db = SessionLocal()

    try:
        student = (
            db.query(Student)
            .filter(Student.id == student_id)
            .first()
        )

        if not student:
            return {
                "success": False,
                "message": f"Student with ID {student_id} was not found."
            }

        student_name = student.name

        db.delete(student)
        db.commit()

        return {
            "success": True,
            "message": f"Student {student_id} ({student_name}) deleted successfully."
        }

    finally:
        db.close()


@tool
def search_students_by_name(name: str) -> list:
    """
    Search for students by name or partial name.
    """

    db = SessionLocal()

    try:
        students = (
            db.query(Student)
            .filter(Student.name.ilike(f"%{name}%"))
            .all()
        )

        return [
            {
                "id": student.id,
                "name": student.name,
                "department": student.department,
                "email": student.email,
                "gpa": student.gpa
            }
            for student in students
        ]

    finally:
        db.close()


student_tools = [
    get_student,
    get_all_students,
    find_students_by_department,
    find_students_by_min_gpa,
    update_student_gpa,
    delete_student,
    search_students_by_name,
]
