import numpy as np
w = np.array([[3,7],[5,10]])
p = np.array([[5,6],[3,7]])

print("Adding 4 to every element:\n", w+4)

print("Substract 2 to every element:\n", p-2)

print("Multiply 3 to every element:\n", w*3)

print(" Array  sum of elements:\n",w+p)

print("Sum of all elements:\n", w.sum())
print("Sum of all elements:\n", w.sum())

#datatypes in numpy
#Every numpy as a datatype
Y = np.array([4,9])
print(Y.dtype)

X = np.array([1,3,4,6], dtype ='float')
print(X.dtype)
