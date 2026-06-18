#using inbuilt math module
import math
pie = math.pi
print("Value of pi", pie)

import pandas
#create a simple dataframe

data = {
    "Name":["John","Mark"],
    "Age": [20,40]
}

print(data)
df = pandas.DataFrame(data)
print(df)