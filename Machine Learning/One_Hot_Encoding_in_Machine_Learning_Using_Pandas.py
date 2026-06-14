import pandas as pd

data = {
    "Employee_ID": [10, 20, 15, 25, 30],
    'Gender': ['M', 'F', 'F', 'M', 'F'],
    'Remarks': ['Good', 'Nice', 'Good', 'Great', 'Nice']
}

df = pd.DataFrame(data)

print("Original Data: ")
print(df)

encoded_df = pd.get_dummies(
    df,
    columns=['Gender', 'Remarks'],
    drop_first=True
)

print("\nOne-Hot Encoded Data: ")
print(encoded_df)