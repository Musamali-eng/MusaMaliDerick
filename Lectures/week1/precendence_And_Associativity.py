#precendence and associativity
#a = 19
#b = 20
#c = 30
#print(a+b*c)

#overriding precendence
#print((a+b)*c)

#print(a%b)

#print(a-b*(a+b)/(c-b))

#If statements
cars = ["honda","nissan patrol","alphard","subaru"]
for car in cars:

  if car == ("honda"):
    print(car.upper())
  else:
    print(car.title())

cars = ["honda","nissan patrol","alphard","subaru"]
for car in cars:

  if car == ("honda"):

    print(car.upper())
  else:
    print(car.title())

# comparing ineguality
car = "bmw"

print(car == "bmw")

print(car == "Bmw")   

#checking for inequality
car = "nissan"
print(car.lower() == "Nissan")

toppings = ["mashrooms", "Banana", "Cassava", "Sweetpatato"]

for topping in toppings:
    if topping in ["Banana", "Cassava", "Sweetpatato"]:
        print(topping.upper())
    else:
        print(topping.title())

# Using AND to check multiple conditions in comparison operators
#Both conditions must be true

#age = int(input("Enter your age: "))

#if age >= 18 and age <= 30:
 #   print("You are eligible to get a National ID")
#else:
  #  print("You are not eligible to get a National ID")

#print(f"Your age is {age} years old!")

# Using OR operator
#At least one condition must be true

#number = int(input("Enter your years: "))

#if number == 18 or number == 30:
 #   print("You are eligible to vote")
#else:
 #   print("You are not eligible to vote")


#print(f"You are {number} years old")

# Precedence of or & and
meal = input("Enter the Name of your favorite dish: ")

money = 5  

if (meal == "fruit" or meal == "sandwich") and money >= 2:
    print("Lunch being delivered")
else:
    print("Can't deliver lunch")
    print(f"Your favorite dish {meal} is not available no delivery made!")