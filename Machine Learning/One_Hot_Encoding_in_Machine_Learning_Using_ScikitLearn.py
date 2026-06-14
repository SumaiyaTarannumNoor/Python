import pandas as pd 
from sklearn.preprocessing import OneHotEncoder

data = {
    'Employee_ID': [10, 20, 15, 25, 30],
    'Gender': ['M', 'F', 'F', 'M', 'F'],
    'Remarks': ['Good', 'Nice', 'Good', 'Great', 'Nice']
}

df = pd.DataFrame(data)

print("Original Data: ")
print(df)

categorical_columns = df.select_dtypes(include=[object]).columns

encoder = OneHotEncoder(sparse_output=False)

encoded_data = encoder.fit_transform(df[categorical_columns])

encoded_df = pd.DataFrame(
    encoded_data,
    columns=encoder.get_feature_names_out(categorical_columns)
)

final_df = pd.concat(
    [df.drop(columns=categorical_columns), encoded_df],
    axis=1
)

print("\nOne-hot Encoded Data: ")
print(final_df)