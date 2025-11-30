import pandas as pd

# This mimics a messy client file with weird headers and random order
data = {
    'empl_id': [101, 102, 103],
    'useless_col_1': ['x', 'y', 'z'],  # Junk column
    'ph_no': ['555-0100', '555-0101', '555-0102'],
    'l_name': ['Doe', 'Smith', 'Jones'],
    'manager_comments': ['Good', 'N/A', 'Promote'], # Junk column
    'curr_sal': [60000, 75000, 82000],
    'fname': ['John', 'Jane', 'Tom']
}

df = pd.DataFrame(data)
df.to_excel("legacy_data.xlsx", index=False)
print("Dummy file 'legacy_data.xlsx' created successfully!")