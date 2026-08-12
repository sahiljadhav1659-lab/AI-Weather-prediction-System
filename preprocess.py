import pandas as pd

# Load the dataset
df = pd.read_csv("dataset/weather.csv")

print("Original Dataset Shape:", df.shape)

# Remove duplicate rows
df = df.drop_duplicates()

# Convert 'date' column to datetime
df["date"] = pd.to_datetime(df["date"])

# Sort the data by date
df = df.sort_values(by="date")

# Reset index
df = df.reset_index(drop=True)

# Display information
print("\nCleaned Dataset Shape:", df.shape)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nData Types:")
print(df.dtypes)

# Save cleaned dataset
df.to_csv("dataset/clean_weather.csv", index=False)

print("\n✅ Cleaned dataset saved successfully!")