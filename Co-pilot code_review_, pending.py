import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Load the dataset
data = pd.read_csv('data.csv')

# Step 2: Basic Data Analysis
# View the first few rows of the dataset
print("First 5 rows of the dataset:")
print(data.head())

# Get summary statistics of the dataset
print("\nSummary statistics:")
print(data.describe())

# Check for missing values
print("\nMissing values in each column:")
print(data.isnull().sum())

# Step 3: Data Visualization
# Plot the distribution of a numeric column (e.g., 'age')
plt.figure(figsize=(10, 6))
data['age'].hist(bins=30)
plt.title('Age Distribution')
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.show()

# Plot a scatter plot between two numeric columns (e.g., 'age' and 'salary')
plt.figure(figsize=(10, 6))
plt.scatter(data['age'], data['salary'])
plt.title('Age vs Salary')
plt.xlabel('Age')
plt.ylabel('Salary')
plt.show()

# Step 4: Grouping and Aggregation
# Example: Group by a categorical column (e.g., 'department') and calculate mean salary
grouped_data = data.groupby('department')['salary'].mean()
print("\nMean salary by department:")
print(grouped_data)
