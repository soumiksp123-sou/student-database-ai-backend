
import chromadb

# Create persistent ChromaDB client
client = chromadb.PersistentClient(path="./chroma_db")

# Create or retrieve collection
collection = client.get_or_create_collection(
    name="students"
)


def add_student_to_vector_store(student):
    """
    Add a student record to ChromaDB.
    """

    document = (
        f"Student ID: {student.id}. "
        f"Name: {student.name}. "
        f"Age: {student.age}. "
        f"Gender: {student.gender}. "
        f"Department: {student.department}. "
        f"Email: {student.email}. "
        f"Phone: {student.phone}. "
        f"GPA: {student.gpa}."
    )

    collection.upsert(
        ids=[str(student.id)],
        documents=[document],
        metadatas=[
            {
                "student_id": student.id,
                "name": student.name,
                "department": student.department,
                "gpa": student.gpa
            }
        ]
    )


def search_students(query, n_results=5):
    """
    Search student records using semantic similarity.
    """

    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    return results
