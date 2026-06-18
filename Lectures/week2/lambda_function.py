#Lambda function in python

#LabActivity
#simple lambda function
#lambda arguments:expression

square = lambda x : x*x
#print(square(5))

#practical application 
#using lambda with filter

#numbers = [8,3,7,40]
#filter even numbers
#evens = list(filter(lambda x: x% 2== 0, numbers))
#print(evens)

#exercise2
#using lambda with sorted()

#fruit = ["mango", "Orange", "Banana", "Pawpaw"]

#sorted_fruits = sorted(fruit, key=lambda x: x.lower())

#print(sorted_fruits)
#ort fruits by length of the name

#fruit = ["mango", "Orange", "Banana", "Pawpaw"]

#sorted_fruits = sorted(fruit, key=lambda x: len(x))

#print(sorted_fruits)

#exercise3
#using Fibonacci sequence get the first 10 fibonacci number in range of 10
def fibonacci(n):
    if n == 0:      # base case
        return 0
    elif n == 1:    # base case
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)

for i in range(10):
    print(fibonacci(i), end=" ")