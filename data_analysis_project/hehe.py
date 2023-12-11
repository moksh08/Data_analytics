import pandas as pd

# Assuming 'your_excel_file.xlsx' is your Excel file
df = pd.read_csv('C:\\Users\\moksh\\Downloads\\cleaned_flight_data (1).csv')

# Get column names
column_names = df.columns

# Now, 'column_names' will be a pandas Index object containing the names of all columns
print(column_names)
