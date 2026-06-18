#Create a program that uses function to display student information, your output should display, name ,age ,course studentnumber
def display_student_info(name, age, course, student_number):
    print("Student Information")
    print("-------------------")
    print(f"Name: {name}")
    print(f"Age: {age}")
    print(f"Course: {course}")
    print(f"Student Number: {student_number}")

# Get input from the user
name = input("Enter student name: ")
age = int(input("Enter age: "))
course = input("Enter course: ")
student_number = input("Enter student number: ")

# Call the function
display_student_info(name, age, course, student_number)