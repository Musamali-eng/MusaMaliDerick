# ==========================================
# ONLINE LEARNING PLATFORM
# Demonstrating Multilevel Inheritance
# ==========================================

# Parent Class
class User:
    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = email

    def login(self):
        print(f"{self.name} has logged in.")

    def logout(self):
        print(f"{self.name} has logged out.")


# Child Class
class Student(User):
    def __init__(self, user_id, name, email, course):
        super().__init__(user_id, name, email)
        self.course = course

    def enroll_course(self):
        print(f"{self.name} is enrolled in {self.course}.")


# Grandchild Class
class TeachingAssistant(Student):
    def __init__(self, user_id, name, email, course, assigned_course):
        super().__init__(user_id, name, email, course)
        self.assigned_course = assigned_course

    def assist_teaching(self):
        print(
            f"{self.name} is assisting in teaching "
            f"{self.assigned_course}."
        )


# ==========================================
# MAIN PROGRAM
# ==========================================

ta = TeachingAssistant(
    "TA001",
    "Musa Mali Derick",
    "musamali@gmail.com",
    "Bachelor of Software Engineering",
    "Object-Oriented Programming"
)

print("===== TEACHING ASSISTANT DETAILS =====")

# Method inherited from User
ta.login()

# Method inherited from Student
ta.enroll_course()

# Method of TeachingAssistant
ta.assist_teaching()

# Another method inherited from User
ta.logout()

print("\n" + "=" * 50)

# Demonstrating inherited attributes
print("User ID:", ta.user_id)
print("Name:", ta.name)
print("Email:", ta.email)
print("Course:", ta.course)
print("Assigned Course:", ta.assigned_course)

print("\n" + "=" * 50)

# Display Method Resolution Order
print("METHOD RESOLUTION ORDER (MRO)")
for cls in TeachingAssistant.mro():
    print(cls.__name__)