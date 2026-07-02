#bar() function takes a list one for category labels(x-axis) and one for thier corresponding values(y-axis)
import matplotlib.pyplot as plt
x = ['A', 'B', 'C', 'D']
y = [3, 7, 2, 5]
plt.bar(x, y) # draws a vertical bar chart using given x and y values
plt.show()