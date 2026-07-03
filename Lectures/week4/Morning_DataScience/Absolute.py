import pandas as pd
import numpy as np


df = pd.read_csv('Housing.csv')
df = df.select_dtypes(include=[np.number]) #selecting only numeric columns

print(df.head()) 

max_abs = np.max(np.abs(df), axis=0) #Calculates the maximum absolute value for each column.
scaled_df = df / max_abs #Divides each value by the maximum absolute value of its column to scale the data.
print(scaled_df.head())