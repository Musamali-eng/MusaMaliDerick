#Pie chars show the share of each category in a dataset. It is a circular chart that is divided into slices to illustrate numerical proportion. The size of each slice is proportional to the quantity it represents.
#The pie() function takes a list of values and optional labels to represent each slice of the pie
import matplotlib.pyplot as plt
labels = ['Python','Java','C++','JavaScript']
sizes = [40,30, 20,10]
# Create a pie chart
plt.pie(sizes, labels = labels, autopct = '%1.1f%%')# Creates a pie chart with slice sizes from sizes, labels for each slice and autopct shows percentage values with one place
# Display the chart
plt.show()