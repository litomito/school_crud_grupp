# TODO download all the imports in your venv
# pip install requests 

import requests
import pyinputplus as pyip

BASE_URL = "http://127.0.0.1:8000/students/"

def create_student():
    name = pyip.inputRegex(r"^[A-Za-z\s]+$", prompt="Enter Name: ")
    age = pyip.inputInt("Enter Age: ")
    gender = pyip.inputChoice(["Male", "Female"])
    height = pyip.inputInt("Enter Height: ")
    grade = pyip.inputRegex(r'^[1-9][A-Ea-e]$', prompt="Enter a grade (1-9, A-E): ").upper()

    student = {
        "name": name,
        "age": age,
        "gender": gender,
        "height": height,
        "grade": grade
    }
    response = requests.post(BASE_URL, json = student)

    if response.status_code == 200:
        print("Student created successfully.")
    else:
        print("Error creating student:", response.json().get("detail", "Unknown error"))

def show_student_cards():
    response = requests.get(BASE_URL)
    
    if response.status_code == 200:
        students = response.json()
        
       
        card_template = (
            "+---------------------------+\n"
            "| Name: {name:<20}|\n"
            "| Age: {age:<21}|\n"
            "| Grade: {grade:<19}|\n"
            "| Gender: {gender:<18}|\n"
            "| Height: {height:<18}|\n"
            "| ID: {id:<22}|\n"
            "+---------------------------+"
        )
        
        
        for student in students:
            card = card_template.format(
                name = student["name"][:20],
                age = student["age"],
                grade = student["grade"],
                gender = student["gender"][:18],
                height = student["height"],
                id = student["id"]
            )
            
            print(card)
    else:
        print("Error fetching students:", response.status_code, response.json())



create_student()
show_student_cards()


# def main():
    