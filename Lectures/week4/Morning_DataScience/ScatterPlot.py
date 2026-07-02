#Scatter plots are used for displaying individual data points and showing the relationship between two variables.
#The scatter() function takes two lists like plot(), but it only plots the individual points without connecting them with lines.
import matplotlib.pyplot as plt
x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]
plt.scatter(x, y)#plots individual data points as dots at specified x and y coordinates
plt.show()