# TODO download all the imports in your venv
# pip install fastapi uvicorn pydantic

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class StudentCreate(BaseModel):
    name: str
    age: int
    gender: str
    height: int
    grade: str

class Student(StudentCreate):
    id: int

students_db: List[Student] = []

@app.get("/students/", response_model=List[Student])
def get_students():
    return students_db

@app.post("/students/", response_model=Student)
def create_student(student: StudentCreate):
    auto_id = max((s.id for s in students_db), default = 0) + 1
    student_with_id = Student(id = auto_id, **student.model_dump())
    students_db.append(student_with_id)
    return student_with_id


@app.get("/students/{student_name}", response_model=Student)
def get_student(student_name: str):
    for student in students_db:
        if student.name == student_name:
            return student
    raise HTTPException(status_code=404, detail="Student not found")
