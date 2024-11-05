# TODO download all the imports in your venv
# pip install requests 

import requests
import pyinputplus as pyip

BASE_URL = "http://127.0.0.1:8000/students/"

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
#Function that shows all students in a card like-template. If unsuccessful, prints error.
def show_all_students():
    response = requests.get(BASE_URL)
    
    if response.status_code == 200:
        students = response.json()
        
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

#Search a student by name and returns only that student information.
def get_student_by_name():
    name = pyip.inputRegex(r"^[A-Za-z\s]+$", prompt="Enter Name: ")
    response = requests.get(BASE_URL + name)
    
    if response.status_code == 200:
        student = response.json()

        card = card_template.format(
            name = student["name"][:20],
            age = student["age"],
            grade = student["grade"],
            gender = student["gender"][:18],
            height = student["height"],
            id = student["id"]
        )
        
        print(card)


def update_student(student_id: int):
    # Prompt the user to select the field they want to update
    change = pyip.inputChoice(["name", "age", "grade", "gender", "height"])
    update_data = {}

    # Collect the updated data based on the user's choice
    match change:
        case "name":
            update_data["name"] = pyip.inputRegex(r"^[A-Za-z\s]+$", prompt = "Enter new name: ")
        case "age":
            update_data["age"] = pyip.inputInt("Enter new age: ")
        case "grade":
            update_data["grade"] = pyip.inputRegex(r'^[1-9][A-Ea-e]$', prompt = "Enter new grade (1-9, A-E): ").upper()
        case "gender":
            update_data["gender"] = pyip.inputChoice(["Male", "Female"])
        case "height":
            update_data["height"] = pyip.inputInt("Enter new height: ")

    # Send the PUT request to update the student
    response = requests.put(f"{BASE_URL}{student_id}", json = update_data)

    if response.status_code == 200:
        print("Student record updated successfully.")
        return response.json()
    elif response.status_code == 404:
        print("Student not found.")
    else:
        print(f"Failed to update student record: {response.status_code}, {response.json()}")


def delete_student(student_id: int):
    response = requests.delete(f"{BASE_URL}{student_id}")
    
    if response.status_code == 200:
        print("Student record deleted successfully.")
        return response.json() 
    elif response.status_code == 404:
        print("Student not found.")
    else:
        print("Failed to delete student record.")


def main():
    while True:
        print("1. Create Student\n2. Show All Students\n3. Get Student by Name\n4. Update Student\n5. Delete Student\n6. Exit")
        choice = pyip.inputInt("Enter choice: ", min = 1, max = 6)
        match choice:
            case 1:
                create_student()
            case 2:
                show_all_students()
            case 3:
                get_student_by_name()
            case 4:
                student_id = pyip.inputInt("Enter Student ID: ")
                update_student(student_id)
            case 5:
                student_id = pyip.inputInt("Enter Student ID: ")
                delete_student(student_id)
            case 6:
                break

if __name__ == "__main__":
    main()