# Using the super() method in inheritance

class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def info(self):
        print("Student Name:", self.name)


# Define child class
class Lecturer(Student):
    def __init__(self, name, age, course):
        # Using super() method
        super().__init__(name, age)
        self.course = course

    def details(self):
        print(self.name, "is a lecturer of", self.course)


z = Lecturer("Agaba", 35, "OOP")
z.info()
z.details()