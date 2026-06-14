#without dict function
student= {
    "Name": "Musa Mali Derick",
    "Age": 25,
    "City": "Kampala"
}

print(student)

#using dict function
student2 = dict(Name = "Akwe John Amos", Age = 30, City = "Masaka")
print(student2)

#accessing dictionary item
print(student2["Name"])

#using get method
print(student2.get("Age"))

#adding and updating dictionary items
student2["Course"] = "Computer Science"
print(student2)

#removing items from dictionary
del student2["City"]
print(student2)

#using pop() method
age = student2.pop("Age")
print(age)

#using items() method to iterate through dictionary
#it returns a view object that displays a list of a dictionary's key-value tuple pairs
for key, value in student2.items():
    print(key, value)

#using nested dictionary
#having a dictionary inside another dictionary
student3 = {
    "name": "Musa Mali Derick",
    "age": 25,
    "city": "Kampala",
    "course": "Software Engineering"
}
print(student3)