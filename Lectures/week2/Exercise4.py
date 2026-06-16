# Global variable
name = "Derick"

def display_name():
    # Local variable
    age = 20

    print("Inside function:")
    print("Name:", name)  # Accessing global variable
    print("Age:", age)    # Accessing local variable

display_name()

print("\nOutside function:")
print("Name:", name)      # Global variable can be accessed here

# print(age)  # This would cause an error because age is local