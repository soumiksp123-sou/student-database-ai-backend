# Student Database Application System – AI Backend

## Project Overview

The Student Database Application System is a modular backend application designed to manage student information and provide an AI-powered interface for interacting with the student database.

The system combines a RESTful backend with an AI chatbot. Users can retrieve and manage student information through APIs, while the AI chatbot can understand natural-language questions and use database tools to obtain the required information.

## Objectives

- Develop a structured student database backend.
- Implement CRUD operations for student records.
- Provide REST APIs using FastAPI.
- Integrate Google Gemini for natural-language interaction.
- Use LangChain and LangGraph for AI agent and tool-calling workflows.
- Use ChromaDB as a vector store.
- Provide a web-based chatbot interface.
- Create a backend architecture that can be deployed as a web service.

## Key Features

### Student Database

- Create student records.
- Retrieve individual student records.
- Retrieve multiple student records.
- Update student information.
- Delete student records.
- Search students using different criteria.

### REST API

The backend is implemented using FastAPI and provides endpoints for:

- Student retrieval
- Student creation
- Student updating
- Student deletion
- AI chatbot interaction

### AI Chatbot

The chatbot allows users to ask questions about students using natural language.

Example:

> What is the name, department, and GPA of student 5?

The AI agent can identify the appropriate database tool, retrieve the student information, and generate a natural-language response.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| FastAPI | REST API framework |
| Uvicorn | ASGI server |
| SQLite | Student database |
| SQLAlchemy | Database ORM |
| Pydantic | Data validation |
| Google Gemini | Large Language Model |
| LangChain | LLM integration |
| LangGraph | AI agent workflow |
| ChromaDB | Vector store |
| HTML/CSS/JavaScript | Chatbot interface |
| ngrok | Public development access |

## Project Structure

```text
student-database-ai-backend/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── tools.py
│   ├── chatbot.py
│   ├── vector_store.py
│   ├── seed.py
│   │
│   └── static/
│       └── index.html
│
├── requirements.txt
├── .gitignore
└── README.md
