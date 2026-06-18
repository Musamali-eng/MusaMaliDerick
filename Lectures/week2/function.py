#functions in python
#built-in functions
#Example of built-in functions
print("Hello world!") #This will print Hello world! to the console
print(len("Hello world!")) # This will return the length of the string "Hello world!" which is 12

#def greet():
 #print("Welcome to Python programming!")
#Calling a function     
#greet() #This will call the greet and print welcome to the python programming
#greet() #You can call the function multiple times to reuse the code


#LabAcitivity2:Mathematical function
#square of number num = 5
#def square_number():
   # num = 5
    #square  = num * num
   # print(square)
#calling the function
#square_number()

#parameters
def greet_user(name):
 print(f"My name is", name)

#arguments
#example of argument
greet_user("Mark")# this is an argument

greet_user ("mark john")

# Fuction with a single parameter
#def greet(name):
 # print(f"My name is", name)
#greet("Mukisa Mark")

#multiple parameter
#def add_numbers(a,b):
   # print(a+b)

#add_numbers(10,20)

#LabActivity
#positional arguments
def display(name,age):
  print(name)
  print(age)
display("Juma Sadamu",30)

#keyword arguments
#arguments that can be specified using parameter name
def display(name,age):
  print(name)
  print(age)
display(name = "Alex Ssemanda",age=30)

#difault paramer 
#Is assigned if no argument is provided
def greet(name = "Sserwada Tom"):
 print(f"Hello you are welcome to python function", name)
greet()
greet("Paul SSemwanga")

#Return Statement
#sends a value back to the caller
#labactivity
# Return Statement
# Sends a value back to the caller

def add(a, b):
    return a * b

result = add(40,8)
print(result)

# Multiple return values

def Calculator(a, b):
    return a + b, a - b

sum_result, diff_result = Calculator(20, 3)

print("Sum =", sum_result)
print("Difference =", diff_result)


#variable scope
#local variable accessed inside the function


def myfunction():
   a = 10
   b = 20
   print("variable a:", a)
   print("variable b:", b)
   return a+b
   
print (myfunction())

#global variable
name = "Python programming"
marks = 80

def myfunction():
#accessing inside the function 
 print("Name:",name)
 print("Marks:", marks)
#function call
myfunction()