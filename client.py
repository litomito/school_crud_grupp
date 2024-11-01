# TODO download all the imports in your venv
# pip install requests pyinputplus

import requests #type: ignore
import pyinputplus as pyip #type: ignore

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

def update_student():
    student_name = pyip.inputRegex(r"^[A-Za-z\s]+$", prompt="Enter Name: ")
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        students = response.json()
    for student in students:
        if student_name == student["name"]:
            return student
    choose_id = pyip.inputInt("Enter ID: ")
    if choose_id in student["id"]:
        change = pyip.inputStr("What do you want to change? ").lower()
        match change:
            case "name":
                name_change = pyip.inputRegex(r"^[A-Za-z\s]+$", prompt="Enter New Name: ")
                student["name"] = name_change
                return student["name"]
            case "age":
                age_change = pyip.inputInt("Enter the students new age: ")
                student["age"] = age_change
                return student["age"]
            case "grade":
                grade_change = pyip.inputRegex(r'^[1-9][A-Ea-e]$', prompt="Enter the students new grade (1-9, A-E): ").upper()
                student["grade"] = grade_change
                return student["grade"]
            case "height":
                height_change = pyip.inputInt("Enter New Height: ")
                student["height"] = height_change
                return student["height"]
    else:
        print("Student id is not in the system!")
        main()




def main():
    while True:
        chosen = pyip.inputInt("1. Create a Student\n2. Show a Student\n3. Update Student\n4. Delete student\n5. Exit\nChoose what to do: ")
        match chosen:
            case 1:
                create_student()
            case 2:
                show_student_cards()
            case 3:
                update_student()
            case 4:
                #delete_student()
                pass
            case 5:
                exit()
        
main()