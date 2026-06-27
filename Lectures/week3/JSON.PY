#JSON PROCESSING
#Example
{
    "Name": "Opio Godgrey",
    "Age" : "24",
    "Course": "Computer Scince",
    "Subject": ["Machine Learning","Python"]
}

#Writing a json file
import json
student = {
    "Name": "Opio Godgrey",
    "Age" : "24",
    "Course": "Computer Scince",
    "Grade": "A",
    "Subject": ["Machine Learning","Python"]
}
#write to the json file
with open('student.json','w') as file:
    json.dump(student, file, indent = 4)
    print('JSON file created successfuly')

#Reaing from json file
with open('student.json','r') as file:
    data = json.load(file)

    #accessing data
    print(f"Student Name: {data['Name']}")
    print(f"Age: {data['Age']}")
    print(f"Course: {data['Course']}")

    print(f"Subject: {', '.join(data['Subject'])}")


# JSON string
json_string = '{"name": "Alice", "age": 25, "Kampala": "Uganda"}'

# Parse JSON string to Python dictionary
data = json.loads(json_string)
print(data['name']) 
print(data['age'])


# Python dictionary
student = {
    "name": "Omara",
    "age": 22,
    "courses": ["Math", "Physics"]
}

# Convert to JSON string
json_string = json.dumps(student, indent=2)
print(json_string)


# Step 1: Create student data
student_data = {
    "student_id": "S001",
    "name": "Okello Tom",
    "age": 20,
    "courses": ["Computer Science", "Mathematics"],
    "grades": {
        "Python": 85,
        "Data Science": 92,
        "Machine Learning": 78
    },
    "is_active": True
}

with open('student_data.json', 'w') as file:
    json.dump(student_data, file, indent=4)
print("Student data saved to JSON!")

with open('student_data.json', 'r') as file:
    loaded_data = json.load(file)

print("\nStudent Information")
print(f"ID: {loaded_data['student_id']}")
print(f"Name: {loaded_data['name']}")
print(f"Age: {loaded_data['age']}")
print(f"Active: {loaded_data['is_active']}")
print("\nCourses")
for course in loaded_data['courses']:
    print(f"- {course}")
print("\nGrades")
for subject, score in loaded_data['grades'].items():
    print(f"- {subject}: {score}")
    
average = sum(loaded_data['grades'].values()) / len(loaded_data['grades'])
print(f"\nAverage Grade: {average:.2f}")
