
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel

from .database import Base, engine, get_db
from . import crud, schemas
from .chatbot import ask_student_database


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Student Database Application System",
    description="Backend for Student Database with AI Chatbot",
    version="1.0.0"
)


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str


@app.get("/")
def root():
    return {
        "message": "Student Database API is running",
        "version": "1.0.0"
    }


@app.get("/students/", response_model=list[schemas.StudentResponse])
def get_students(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return crud.get_students(db, skip=skip, limit=limit)


@app.get("/students/{student_id}", response_model=schemas.StudentResponse)
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = crud.get_student(db, student_id)

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


@app.post(
    "/students/",
    response_model=schemas.StudentResponse,
    status_code=201
)
def create_student(
    student: schemas.StudentCreate,
    db: Session = Depends(get_db)
):
    return crud.create_student(db, student)


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


@app.delete("/students/{student_id}")
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


@app.post("/chat/", response_model=ChatResponse)
def chat(request: ChatRequest):

    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    try:
        answer = ask_student_database(request.question)

        return {
            "answer": answer
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.get("/chat-ui", response_class=HTMLResponse)
def chat_ui():
    return FileResponse("app/static/index.html")
