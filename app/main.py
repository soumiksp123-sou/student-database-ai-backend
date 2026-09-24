
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel

from .database import Base, engine, get_db
from . import crud, schemas
from .chatbot import ask_student_database
from .seed import initialize_database


# Initialize database when the application starts
initialize_database()


app = FastAPI(
    title="Student Database Application System",
    description="Backend for Student Database with AI Chatbot",
    version="1.0.0"
)


# ============================================
# Request / Response Models
# ============================================

class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str


# ============================================
# Health Check
# Supports GET and HEAD requests
# ============================================

@app.api_route("/", methods=["GET", "HEAD"])
def root():
    return {
        "message": "Student Database API is running",
        "version": "1.0.0"
    }


# ============================================
# GET ALL STUDENTS
# ============================================

@app.get(
    "/students/",
    response_model=list[schemas.StudentResponse]
)
def get_students(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return crud.get_students(
        db,
        skip=skip,
        limit=limit
    )


# ============================================
# GET STUDENT BY ID
# ============================================

@app.get(
    "/students/{student_id}",
    response_model=schemas.StudentResponse
)
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = crud.get_student(
        db,
        student_id
    )

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


# ============================================
# CREATE STUDENT
# ============================================

@app.post(
    "/students/",
    response_model=schemas.StudentResponse,
    status_code=201
)
def create_student(
    student: schemas.StudentCreate,
    db: Session = Depends(get_db)
):
    return crud.create_student(
        db,
        student
    )


# ============================================
# UPDATE STUDENT
# ============================================

@app.put(
    "/students/{student_id}",
    response_model=schemas.StudentResponse
)
def update_student(
    student_id: int,
    student: schemas.StudentUpdate,
    db: Session = Depends(get_db)
):
    updated_student = crud.update_student(
        db,
        student_id,
        student
    )

    if not updated_student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return updated_student


# ============================================
# DELETE STUDENT
# ============================================

@app.delete(
    "/students/{student_id}"
)
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    deleted_student = crud.delete_student(
        db,
        student_id
    )

    if not deleted_student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return {
        "message": "Student deleted successfully",
        "student_id": student_id
    }


# ============================================
# AI CHAT API
# ============================================

@app.post(
    "/chat/",
    response_model=ChatResponse
)
def chat(request: ChatRequest):

    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    try:
        answer = ask_student_database(
            request.question
        )

        return {
            "answer": answer
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================
# CHATBOT WEB UI
# ============================================

@app.get(
    "/chat-ui",
    response_class=HTMLResponse
)
def chat_ui():
    return FileResponse(
        "app/static/index.html"
    )
