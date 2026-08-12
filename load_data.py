import pandas as pd

# Load the dataset
df = pd.read_csv("dataset/weather.csv")

# Display the first 5 rows
print("First 5 Rows:")
print(df.head())

# Display dataset shape
print("\nDataset Shape:")
print(df.shape)

# Display column names
print("\nColumns:")
print(df.columns)

# Display missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Display data types
print("\nData Types:")
print(df.dtypes)