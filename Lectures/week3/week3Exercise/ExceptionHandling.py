# Custom Exception
class DrivingAgeError(Exception):
    pass

# Function to check driving eligibility
def drive_car(name, age):
    if age < 18:
        raise DrivingAgeError(
            f"{name} is not allowed to drive in Uganda. Minimum age is 18."
        )
    print(f"{name} is allowed to drive a car in Uganda.")

# Get user input
name = input("Enter your name: ")
age = int(input("Enter your age: "))

# Check eligibility
try:
    drive_car(name, age)
except DrivingAgeError as e:
    print("Error:", e)