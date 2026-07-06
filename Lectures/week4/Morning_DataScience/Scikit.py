#Scikit library week 4 morning data science lecture by Dr Livingstone
#It's open source library for machine learning in python
#It provides tools data analysis and predictive modeling

#Feature of Scikit-learn
#1. Data preprocessing it involves data splitting,Feature scaling, feature selection and feature extraction
# Data splitting: It involves training and testing data.
#3. Model selection
#4. Evaluation

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