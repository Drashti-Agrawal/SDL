import pandas as pd

# Example DataFrame
data = {
    'Column1': ['Data1', '', 'Data2'],
    'Column2': ['', 'Data3', ''],
    'Column3': ['Data4', '', 'Data5'],
}
df = pd.DataFrame(data)

# Initialize the map (dictionary)
map_dict = {}

# Specify the row number you want to check, here using row 1 as an example
row_number = 0

# Loop through the columns starting from index 0 to the length of the row
for i in range(3, len(df.columns)):  # Adjust the range as needed
    # Get the value in the specified row and column
    sub = ''  # Access the specific row and column   df.iat[row_number, i]
    
    if pd.notna(df.iat[row_number, i]):  # Check if the column is not empty
        sub = df.iat[row_number, i] # Store the value in a sub variable
        
        map_dict[sub] = []  # Initialize the list if the key does not exist
        map_dict[sub].append(i)  # Append the column index to the list
    else:
        
        map_dict[sub].append(i)  # Append the column index to the list

# Print the resulting map
print(map_dict)
