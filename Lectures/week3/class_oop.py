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

#class Student:
  #  name = "Akwe John Amos"
   # Nationality = "Ugandan"
    
    # Using __init__()
   # def __init__(self, age, religion):
   #     self.age = age
   #     self.religion = religion

# Create student object
#student1 = Student(21, "BornAgain")

#print(student1.age)        
#print(student1.religion)  
#print(student1.name)       
#print(student1.Nationality)

#Exercise for morging sessio about class in pyhthon using OOP
class Restaurant:
    def __init__(self, restaurant_name, cuisine_type):
        self.restaurant_name = restaurant_name
        self.cuisine_type = cuisine_type
    
    def describe_restaurant(self):
        print(f"Restaurant Name: {self.restaurant_name}")
        print(f"Cuisine Type: {self.cuisine_type}")
    
    def open_restaurant(self):
        print(f"{self.restaurant_name} is now OPEN!")

restaurant = Restaurant("Taste of Africa", "Ugandan")


print(f"Restaurant: {restaurant.restaurant_name}")
print(f"Cuisine: {restaurant.cuisine_type}")
print()

# Call both methods
restaurant.describe_restaurant()
restaurant.open_restaurant()

#Three Restaurant
class Restaurant:
    def __init__(self, restaurant_name, cuisine_type):
        self.restaurant_name = restaurant_name
        self.cuisine_type = cuisine_type
    
    def describe_restaurant(self):
        print(f"Restaurant Name: {self.restaurant_name}")
        print(f"Cuisine Type: {self.cuisine_type}")
    
    def open_restaurant(self):
        print(f"{self.restaurant_name} is now OPEN! \n")

restaurant1 = Restaurant("Taste of Africa", "Kampala")
restaurant2 = Restaurant("Kati Kati", "Lugogo")
restaurant3 = Restaurant("Pizza Palace", "Bugolobi")

print(" RESTAURANT DESCRIPTIONS\n")
restaurant1.describe_restaurant()
restaurant2.describe_restaurant()
restaurant3.describe_restaurant()

print("RESTAURANT STATUS\n")
restaurant1.open_restaurant()
restaurant2.open_restaurant()
restaurant3.open_restaurant()

#User profile
class User:
    def __init__(self, first_name, last_name, age, email, location, occupation):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.email = email
        self.location = location
        self.occupation = occupation
    
    def describe_user(self):
    
        print("USER PROFILE")
        print(f"Full Name: {self.first_name} {self.last_name}")
        print(f"Age: {self.age}")
        print(f"Email: {self.email}")
        print(f"Location: {self.location}")
        print(f"Occupation: {self.occupation}")

    
    def greet_user(self):
        print(f"Hello {self.first_name}! Welcome back!\n")

# Create several user instances
user1 = User("Akwe", "Amos", 21, "amos@email.com", "Kampala", "Student")
user2 = User("Sarah", "Nakato", 28, "sarah@email.com", "Entebbe", "Engineer")
user3 = User("John", "Muwonge", 35, "john@email.com", "Jinja", "Teacher")

# Call both methods for each user
print(" USER 1\n")
user1.describe_user()
user1.greet_user()

print("USER 2\n")
user2.describe_user()
user2.greet_user()

print("USER 3\n")
user3.describe_user()
user3.greet_user()