from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, EmailStr
from settings import settings

app = FastAPI(title=settings.app_name, 
            debug=settings.debug, 
            description="API for managing student courses", 
            version="1.0.0")


class StudentCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50, description="Name must be between 1 and 50 characters")
    age: int = Field(gt= 0, lt= 120, description="Age must be a positive integer")
    email: EmailStr

students = [
    {
        "id": 1,
        "name": "John",
        "age": 20,
        "email": "john@example.com"
    },
    {
        "id": 2,
        "name": "Robin",
        "age": 22,
        "email": "robin@example.com"
    }
]
    


@app.get("/")
def home():
    return {"message": "Welcome to the Student Management Course API!"}

@app.get("/students")
def get_students():
    return students

@app.get("/students/{student_id}")
def get_student_by_id(student_id: int):
    for s in students:
        if s["id"] == student_id:
            return s
    raise HTTPException(status_code=409, details="Student not found")
    

@app.post("/students")
def create_student(student_create: StudentCreate):
    for existing_student in students:
        if existing_student["email"] == student_create.email:
            raise HTTPException(
                status_code=409, 
                detail="Email already exists"
            )
        
    new_student = student_create.model_dump()
    
    new_student['email'] = str(student_create.email)
    
    new_student["id"] = max((s["id"] for s in students),default=0) + 1
    
    students.append(new_student)
    return new_student
