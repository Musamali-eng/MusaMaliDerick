
# SOFTWARE ENGINEERING INTERNSHIP PORTAL
# Demonstrates:
# 1. Inheritance
# 2. Method Overriding
# 3. Multiple Inheritance
# 4. Method Resolution Order (MRO)

# Base Class
class User:
    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.logged_in = False

    def login(self):
        self.logged_in = True
        print(f"\n{self.name} has logged in.")

    def logout(self):
        self.logged_in = False
        print(f"{self.name} has logged out.")

    def display_profile(self):
        print("\nUSER PROFILE ")
        print("User ID:", self.user_id)
        print("Name:", self.name)
        print("Email:", self.email)


# Student Class
class Student(User):
    def __init__(self, user_id, name, email, reg_no, course):
        User.__init__(self, user_id, name, email)
        self.reg_no = reg_no
        self.course = course

    # Method overriding
    def display_profile(self):
        print("\nSTUDENT PROFILE")
        print("User ID:", self.user_id)
        print("Name:", self.name)
        print("Email:", self.email)
        print("Registration Number:", self.reg_no)
        print("Course:", self.course)


# Supervisor Class
class Supervisor(User):
    def __init__(self, user_id, name, email, company_name, employee_id):
        User.__init__(self, user_id, name, email)
        self.company_name = company_name
        self.employee_id = employee_id

    # Method overriding
    def display_profile(self):
        print("\nSUPERVISOR PROFILE")
        print("User ID:", self.user_id)
        print("Name:", self.name)
        print("Email:", self.email)
        print("Company Name:", self.company_name)
        print("Employee ID:", self.employee_id)


# Multiple Inheritance
class StudentRepresentative(Student, Supervisor):
    def __init__(
        self,
        user_id,
        name,
        email,
        reg_no,
        course,
        company_name,
        employee_id
    ):
        Student.__init__(self, user_id, name, email, reg_no, course)
        Supervisor.__init__(
            self,
            user_id,
            name,
            email,
            company_name,
            employee_id
        )

    # Method overriding
    def display_profile(self):
        print("\nSTUDENT REPRESENTATIVE PROFILE")
        print("User ID:", self.user_id)
        print("Name:", self.name)
        print("Email:", self.email)
        print("Registration Number:", self.reg_no)
        print("Course:", self.course)
        print("Company Name:", self.company_name)
        print("Employee ID:", self.employee_id)


# MAIN PROGRAM


# Student Object
student = Student(
    "U001",
    "Ruth Nankya",
    "ruth@student.mak.ac.ug",
    "24/U/SE/1010",
    "Bachelor of Software Engineering"
)

student.login()
student.display_profile()
student.logout()

print("\n" + "=" * 50)

# Supervisor Object
supervisor = Supervisor(
    "U002",
    "Sarah Namusoke",
    "snamusoke@mtn.co.ug",
    "MTN Uganda",
    "MTN205"
)

supervisor.login()
supervisor.display_profile()
supervisor.logout()

print("\n" + "=" * 50)

# Student Representative Object
representative = StudentRepresentative(
    "U003",
    "Musa Mali Derick",
    "musamali@gmail.com",
    "23/U/SE/1001",
    "Bachelor of Software Engineering",
    "Centenary Bank",
    "CB102"
)

representative.login()
representative.display_profile()
representative.logout()

print("\n" + "=" * 50)

# Demonstrating Inherited Attributes
print("\nINHERITED ATTRIBUTES")
print("Representative Name:", representative.name)
print("Representative Email:", representative.email)
print("Representative Course:", representative.course)
print("Representative Company:", representative.company_name)

print("\n" + "=" * 50)

# Method Resolution Order (MRO)
print("\nMETHOD RESOLUTION ORDER (MRO)")
for cls in StudentRepresentative.mro():
    print(cls.__name__)