#define a class with class keyword
#class keyword name:
class Dog:

#Define an attribute for my class
    name = "German Shepard"

#An object is a specific instanse of a class. It can have it's own methods, parameters, multiple objects can be created using the same class
#create an object from a class
dog1 = Dog()
print(dog1.name)

#Using a costructor
#create a student

class Student:
    name = "Akwe John Amos"
    Nationality = "Ugandan"
    
    # Using __init__()
    def __init__(self, age, religion):
        self.age = age
        self.religion = religion

# Create student object
student1 = Student(21, "BornAgain")

print(student1.age)        
print(student1.religion)  
print(student1.name)       
print(student1.Nationality)

