class User:
    def __init__(self, first_name,last_name,age,email, occupation):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.email = email
        self.occupation = occupation
    def describe_user(self):
        print("USER PROFILE")
        print(f"Full Name: {self.first_name} {self.last_name}\n")
        print(f"Age: {self.age}\n")
        print(f"Email: {self.email}\n")
        print(f"Occupation: {self.occupation}")
    
    def greet_user(self):
        print(f"Hello {self.first_name}! Welcome back!\n")

user1 = User("Akwe" ,"John Amos", 28, "akwejohnamos@gmail.com", "Water Engineer")
user2 = User("Ochaya" ,"Godfrey",40,"ochayagodgrey@gmail.com","Doctor")
user3 = User("Nakato", "Sarah", 38, "nakatosarah@gmail.com","Software")

print("Water Engineer\n")
user1.describe_user()
user1.greet_user()

print("Doctor\n")
user2.describe_user()
user2.greet_user()

print("Software Engineer\n")
user3.describe_user()
user3.greet_user()

