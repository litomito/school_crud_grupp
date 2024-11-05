# TODO download all the imports in your venv
# pip install fastapi uvicorn pydantic

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Define the data models for the API
class StudentCreate(BaseModel):
    name: str
    age: int
    gender: str
    height: int
    grade: str

class StudentUpdate(BaseModel): # template for all of the new student information
    name: Optional[str] = None 
    age: Optional[int] = None
    gender: Optional[str] = None
    height: Optional[int] = None
    grade: Optional[str] = None

# Define the data model for the response
class Student(StudentCreate):
    id: int

# Create an in-memory database to store the students
students_db: List[Student] = []
#Returns a list of students.
@app.get("/students/", response_model = List[Student])
def get_students():
    return students_db

# Create a new student
@app.post("/students/", response_model = Student)
def create_student(student: StudentCreate):
    # Generate a new ID for the student by adding 1 to the maximum ID in the database
    auto_id = max((s.id for s in students_db), default = 0) + 1
    # Create a new student with the generated ID and the data from the request
    student_with_id = Student(id = auto_id, **student.model_dump())
    students_db.append(student_with_id)
    return student_with_id

#Returns the list. Looks after student name.
@app.get("/students/{student_name}", response_model = Student)
def get_student(student_name: str):
    for student in students_db:
        if student.name == student_name:
            return student
    raise HTTPException(status_code = 404, detail = "Student not found")


@app.put("/students/{student_id}", response_model = Student)
def update_student(student_id: int, student_update: StudentUpdate):
    for student in students_db:
        if student.id == student_id:
            # Update only fields that are provided in the request
            update_data = student_update.model_dump(exclude_unset = True)
            for key, value in update_data.items():
                setattr(student, key, value)
            return student
    raise HTTPException(status_code = 404, detail = "Student not found")


@app.delete("/students/{student_id}", response_model = Student)
def delete_student(student_id: int):
    for index, student in enumerate(students_db):
        if student.id == student_id:
            delete_student = students_db.pop(index)
            return delete_student
    raise HTTPException(status_code=404, detail = "Student not found")
        
