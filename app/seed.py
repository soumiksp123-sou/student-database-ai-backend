
from .database import Base, engine, SessionLocal
from .models import Student
from .vector_store import add_student_to_vector_store


# Create database tables
Base.metadata.create_all(bind=engine)


students_data = [
    {
        "name": "Aarav Sharma",
        "age": 20,
        "gender": "Male",
        "department": "CSE",
        "email": "aarav.sharma@example.com",
        "phone": "9876543210",
        "gpa": 9.1
    },
    {
        "name": "Ananya Das",
        "age": 19,
        "gender": "Female",
        "department": "ECE",
        "email": "ananya.das@example.com",
        "phone": "9876543211",
        "gpa": 8.7
    },
    {
        "name": "Rohan Singh",
        "age": 21,
        "gender": "Male",
        "department": "ME",
        "email": "rohan.singh@example.com",
        "phone": "9876543212",
        "gpa": 8.2
    },
    {
        "name": "Priya Roy",
        "age": 20,
        "gender": "Female",
        "department": "CSE",
        "email": "priya.roy@example.com",
        "phone": "9876543213",
        "gpa": 9.3
    },
    {
        "name": "Aditya Kumar",
        "age": 22,
        "gender": "Male",
        "department": "ECE",
        "email": "aditya.kumar@example.com",
        "phone": "9876543214",
        "gpa": 8.9
    },
    {
        "name": "Sneha Gupta",
        "age": 20,
        "gender": "Female",
        "department": "IT",
        "email": "sneha.gupta@example.com",
        "phone": "9876543215",
        "gpa": 9.0
    },
    {
        "name": "Rahul Das",
        "age": 21,
        "gender": "Male",
        "department": "CSE",
        "email": "rahul.das@example.com",
        "phone": "9876543216",
        "gpa": 8.6
    },
    {
        "name": "Ishita Sen",
        "age": 19,
        "gender": "Female",
        "department": "EE",
        "email": "ishita.sen@example.com",
        "phone": "9876543217",
        "gpa": 8.8
    },
    {
        "name": "Arjun Mehta",
        "age": 22,
        "gender": "Male",
        "department": "IT",
        "email": "arjun.mehta@example.com",
        "phone": "9876543218",
        "gpa": 8.4
    },
    {
        "name": "Meera Nair",
        "age": 20,
        "gender": "Female",
        "department": "CSE",
        "email": "meera.nair@example.com",
        "phone": "9876543219",
        "gpa": 9.2
    },
    {
        "name": "Vikram Patel",
        "age": 21,
        "gender": "Male",
        "department": "CE",
        "email": "vikram.patel@example.com",
        "phone": "9876543220",
        "gpa": 8.1
    },
    {
        "name": "Kavya Iyer",
        "age": 20,
        "gender": "Female",
        "department": "ECE",
        "email": "kavya.iyer@example.com",
        "phone": "9876543221",
        "gpa": 9.4
    },
    {
        "name": "Siddharth Bose",
        "age": 22,
        "gender": "Male",
        "department": "CSE",
        "email": "siddharth.bose@example.com",
        "phone": "9876543222",
        "gpa": 8.5
    },
    {
        "name": "Riya Chatterjee",
        "age": 19,
        "gender": "Female",
        "department": "IT",
        "email": "riya.chatterjee@example.com",
        "phone": "9876543223",
        "gpa": 9.1
    },
    {
        "name": "Dev Malhotra",
        "age": 21,
        "gender": "Male",
        "department": "ME",
        "email": "dev.malhotra@example.com",
        "phone": "9876543224",
        "gpa": 8.3
    }
]


db = SessionLocal()

try:
    existing_count = db.query(Student).count()

    if existing_count == 0:

        for student_data in students_data:
            student = Student(**student_data)

            db.add(student)
            db.commit()
            db.refresh(student)

            add_student_to_vector_store(student)

        print("15 students inserted successfully.")

    else:
        print(f"Database already contains {existing_count} students.")

finally:
    db.close()
