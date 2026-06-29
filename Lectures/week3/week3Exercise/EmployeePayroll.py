# ==========================================
# EMPLOYEE PAYROLL SYSTEM
# ==========================================

# Base Class
class Employee:
    def __init__(self, name, employee_number):
        self.name = name
        self.employee_number = employee_number

    def calculate_pay(self):
        """Method to be overridden by subclasses"""
        pass

    def display_info(self):
        print("\nEmployee Name:", self.name)
        print("Employee Number:", self.employee_number)


# Full-Time Employee Class
class FullTimeEmployee(Employee):
    def __init__(self, name, employee_number, monthly_salary):
        super().__init__(name, employee_number)
        self.monthly_salary = monthly_salary

    # Method overriding
    def calculate_pay(self):
        return self.monthly_salary


# Part-Time Employee Class
class PartTimeEmployee(Employee):
    def __init__(self, name, employee_number, hours_worked, hourly_rate):
        super().__init__(name, employee_number)
        self.hours_worked = hours_worked
        self.hourly_rate = hourly_rate

    # Method overriding
    def calculate_pay(self):
        return self.hours_worked * self.hourly_rate


# ==========================================
# MAIN PROGRAM
# ==========================================

# Create employee objects
employee1 = FullTimeEmployee(
    "Sarah Namusoke",
    "EMP001",
    2500000
)

employee2 = PartTimeEmployee(
    "Musa Mali Derick",
    "EMP002",
    80,
    15000
)

# Polymorphism
employees = [employee1, employee2]

print("===== EMPLOYEE PAYROLL REPORT =====")

for employee in employees:
    employee.display_info()
    print("Monthly Pay: UGX {:,}".format(employee.calculate_pay()))
    print("-" * 40)