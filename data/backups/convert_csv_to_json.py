import pandas as pd
import json

# Load CSV file with specific column handling
df = pd.read_csv('combined_players.csv', dtype=str)

# Select relevant columns based on provided CSV structure
df_selected = df[['display_name', 'position', 'team_abbr', 'college_name']]

# Split display_name into firstName and lastName
def split_display_name(name):
    parts = name.split(' ')
    if len(parts) > 1:
        firstName = ' '.join(parts[:-1])
        lastName = parts[-1]
    else:
        firstName = name
        lastName = ''
    return firstName, lastName

# Apply the split_display_name function
df_selected[['firstName', 'lastName']] = df_selected['display_name'].apply(lambda x: pd.Series(split_display_name(x)))

# Rename other columns
df_selected.rename(columns={
    'position': 'position',
    'team_abbr': 'team',
    'college_name': 'college'
}, inplace=True)

# Clean the data by replacing NaN values with empty strings
df_selected.fillna('', inplace=True)

# Convert DataFrame to JSON format
json_data = df_selected[['firstName', 'lastName', 'position', 'team', 'college']].to_dict(orient='records')

# Save the JSON data to a file
with open('players.json', 'w', encoding='utf-8') as json_file:
    json.dump(json_data, json_file, indent=2)

print(f"Successfully converted {len(df_selected)} records to players.json")