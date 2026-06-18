#write  a function that takes input and calculate area of a rectangle
def rectangle_area():
    length = int(input("Enter the length: "))
    width = int(input("Enter the width: "))
    area = length * width
    print(f"The area of the rectangle is {area}")

rectangle_area()