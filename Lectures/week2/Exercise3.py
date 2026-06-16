def calculate_area(radius):
    area = 3.142 * radius * radius
    return area

# Input from user
radius = float(input("Enter the radius: "))

# Call the function
result = calculate_area(radius)

print(f"The area of the circle is {result}")