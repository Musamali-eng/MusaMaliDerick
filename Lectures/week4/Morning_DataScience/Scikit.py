#Scikit library week 4 morning data science lecture by Dr Livingstone
#Absolute Maximum Scaling
import pandas as pd
import numpy as np

df = pd.read_csv(r'D:\Recess\MusaMaliDerick\Lectures\week4\Morning_DataScience\Housing.csv')
df = df.select_dtypes(include=[np.number]) #selecting only numeric columns
df.head() 
print(df.head()) 
max_abs = np.max(np.abs(df), axis=0) #Calculates the maximum absolute value for each column.
scaled_df = df / max_abs #Divides each value by the maximum absolute value of its column to scale the data.
print(scaled_df.head())