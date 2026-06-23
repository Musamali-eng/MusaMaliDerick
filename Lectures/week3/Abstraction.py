from abc import ABC, abstractmethod

# Abstract class
class Vehicle(ABC):
    
    @abstractmethod
    def start_engine(self):
        pass  # No implementation
    
    @abstractmethod
    def stop_engine(self):
        pass  # No implementation
    
    def display_info(self):  # Regular method (has implementation)
        print("This is a vehicle")


# Child class MUST implement abstract methods
class Car(Vehicle):
    
    def start_engine(self):  # Must implement
        print("Car engine started!")
    
    def stop_engine(self):   # Must implement
        print("Car engine stopped!")


# Child class MUST implement abstract methods
class Motorcycle(Vehicle):
    
    def start_engine(self):  # Must implement
        print("Motorcycle engine started!")
    
    def stop_engine(self):   # Must implement
        print("Motorcycle engine stopped!")


# Testing
# vehicle = Vehicle()  # ERROR! Cannot instantiate abstract class

car = Car()            # OK
car.start_engine()     # Car engine started!
car.stop_engine()      # Car engine stopped!

bike = Motorcycle()    # OK
bike.start_engine()    # Motorcycle engine started!
bike.stop_engine()     # Motorcycle engine stopped!

#exercise
from abc import ABC, abstractmethod
import math

# Abstract class with multiple abstract methods
class Shape(ABC):
    
    @abstractmethod
    def area(self):
        """Calculate the area of the shape"""
        pass
    
    @abstractmethod
    def perimeter(self):
        """Calculate the perimeter of the shape"""
        pass
    
    @abstractmethod
    def display_info(self):
        """Display shape information"""
        pass
    
    def welcome(self):
        print("Welcome to Shape Calculator!")


# Rectangle class implementing all abstract methods
class Rectangle(Shape):
    
    def __init__(self, length, width):
        self.length = length
        self.width = width
    
    def area(self):
        return self.length * self.width
    
    def perimeter(self):
        return 2 * (self.length + self.width)
    
    def display_info(self):
        print("RECTANGLE")
        print(f"Length: {self.length}")
        print(f"Width: {self.width}")
        print(f"Area: {self.area()}")
        print(f"Perimeter: {self.perimeter()}")


# Circle class implementing all abstract methods
class Circle(Shape):
    
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        return math.pi * self.radius ** 2
    
    def perimeter(self):
        return 2 * math.pi * self.radius
    
    def display_info(self):
        print(" CIRCLE")
        print(f"Radius: {self.radius}")
        print(f"Area: {self.area():.2f}")
        print(f"Perimeter: {self.perimeter():.2f}")
print("SHAPE CALCULATOR\n")

rect = Rectangle(10, 5)
rect.welcome()
rect.display_info()

print()

circle = Circle(7)
circle.welcome()
circle.display_info()

print()

print(" COMPARING SHAPES")
shapes = [rect, circle]

for shape in shapes:
    print(f"\nShape: {shape.__class__.__name__}")
    print(f"Area: {shape.area():.2f}")
    print(f"Perimeter: {shape.perimeter():.2f}")