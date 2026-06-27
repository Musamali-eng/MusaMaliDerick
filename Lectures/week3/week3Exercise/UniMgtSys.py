class Person:
    def __init__(self, name, national_id, email, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.national_id = national_id
        self.email = email

    def display_info(self):
        return (
            f"Name: {self.name}\n"
            f"National ID: {self.national_id}\n"
            f"Email: {self.email}"
        )


class Student(Person):
    def __init__(self, registration_number, program_of_study, **kwargs):
        super().__init__(**kwargs)
        self.registration_number = registration_number
        self.program_of_study = program_of_study

    def display_info(self):
        return (
            f"{super().display_info()}\n"
            f"Registration Number: {self.registration_number}\n"
            f"Program of Study: {self.program_of_study}"
        )


class Staff(Person):
    def __init__(self, employee_number, department, **kwargs):
        super().__init__(**kwargs)
        self.employee_number = employee_number
        self.department = department

    def display_info(self):
        return (
            f"{super().display_info()}\n"
            f"Employee Number: {self.employee_number}\n"
            f"Department: {self.department}"
        )


class TeachingAssistant(Student, Staff):
    def __init__(
        self,
        name,
        national_id,
        email,
        registration_number,
        program_of_study,
        employee_number,
        department,
        courses_taught=None,
    ):
        super().__init__(
            name=name,
            national_id=national_id,
            email=email,
            registration_number=registration_number,
            program_of_study=program_of_study,
            employee_number=employee_number,
            department=department,
        )
        self.courses_taught = courses_taught or []

    def display_info(self):
        return (
            f"{super().display_info()}\n"
            f"Courses Taught: {', '.join(self.courses_taught)}"
        )


# Demonstration
def demonstrate():
    student = Student(
        name="Alice Johnson",
        national_id="123-456",
        email="alice@uni.edu",
        registration_number="R001",
        program_of_study="Computer Science",
    )

    staff = Staff(
        name="Dr. Brown",
        national_id="789-012",
        email="brown@uni.edu",
        employee_number="E101",
        department="Engineering",
    )

    ta = TeachingAssistant(
        name="Bob Smith",
        national_id="345-678",
        email="bob@uni.edu",
        registration_number="R002",
        program_of_study="Mathematics",
        employee_number="E102",
        department="Mathematics",
        courses_taught=["Calculus I", "Linear Algebra"],
    )

    print("STUDENT")
    print(student.display_info())

    print("\nSTAFF")
    print(staff.display_info())

    print("\nTEACHING ASSISTANT")
    print(ta.display_info())

    print("\nMRO")
    for cls in TeachingAssistant.mro():
        print(cls.__name__)


demonstrate()