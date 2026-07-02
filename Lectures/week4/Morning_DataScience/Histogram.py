#Histograms are used to visualize the distribution of a dataset. They group data into bins and display the frequency of data points in each bin as bars.
import matplotlib.pyplot as plt
import numpy as np
data = np.random.randn(1000) # generates 1000 random numbers from a normal distribution
plt.hist(data, bins=30, edgecolor='black') # creates a histogram with 30 bins and black edges for the bars
plt.title('Histogram of Random Data') # adds a title to the histogram
plt.xlabel('Value') # adds a label to the x-axis
plt.ylabel('Frequency') # adds a label to the y-axis
plt.show() # displays the histogram