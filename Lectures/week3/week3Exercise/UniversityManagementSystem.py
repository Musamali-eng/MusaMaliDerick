class Person:
    def __init__(self, name, national_id, email):
        self.name = name
        self.national_id = national_id
        self.email = email

    def display_info(self):
        print(f"Name: {self.name}")
        print(f"National ID: {self.national_id}")
        print(f"Email: {self.email}")


class Student(Person):
    def __init__(self, name, national_id, email, reg_no, program):
        super().__init__(name, national_id, email)
        self.reg_no = reg_no
        self.program = program

    def display_info(self):
        super().display_info()
        print(f"Registration Number: {self.reg_no}")
        print(f"Program: {self.program}")


class Staff(Person):
    def __init__(self, name, national_id, email, emp_no, department):
        super().__init__(name, national_id, email)
        self.emp_no = emp_no
        self.department = department

    def display_info(self):
        super().display_info()
        print(f"Employee Number: {self.emp_no}")
        print(f"Department: {self.department}")


class TeachingAssistant(Student, Staff):
    def __init__(self, name, national_id, email, reg_no, program, emp_no, department):
        Student.__init__(self, name, national_id, email, reg_no, program)
        Staff.__init__(self, name, national_id, email, emp_no, department)

    def display_info(self):
        super().display_info()
        print(f"Employee Number: {self.emp_no}")
        print(f"Department: {self.department}")


print("UNIVERSITY MANAGEMENT SYSTEM")
print("=" * 30)

print("\nSTUDENT:")
s = Student("Alice", "ID123", "alice@edu", "REG001", "CS")
s.display_info()

print("\nSTAFF:")
st = Staff("Dr. Smith", "ID456", "smith@edu", "EMP001", "Engineering")
st.display_info()

print("\nTEACHING ASSISTANT:")
ta = TeachingAssistant("Bob", "ID789", "bob@edu", "REG002", "Math", "EMP002", "Math Dept")
ta.display_info()

print("\nMRO:")
print(TeachingAssistant.mro())