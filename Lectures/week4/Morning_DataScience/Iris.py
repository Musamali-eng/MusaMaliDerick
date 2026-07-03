import pandas as pd
import zipfile
import io

zip_path = r'D:\Recess\MusaMaliDerick\Lectures\week4\Morning_DataScience\iris.zip'

# Open the ZIP and extract iris.data
with zipfile.ZipFile(zip_path, 'r') as z:
    with z.open('iris.data') as f:
        # Read the content
        content = f.read().decode('utf-8')
        # Convert to DataFrame
        from io import StringIO
        df = pd.read_csv(StringIO(content), header=None)
        df.columns = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species']

print(df.head())
print(f"\nShape: {df.shape}")