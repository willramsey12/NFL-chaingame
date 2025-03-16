import pandas as pd

# Load CSV file
df = pd.read_csv('players.csv', dtype=str)

# Select only specific columns as requested
df_selected = df[['display_name', 'first_name', 'last_name', 'birth_date', 'college_name',
                  'position', 'jersey_number', 'height', 'weight', 'team_abbr',
                  'draft_club', 'headshot', 'draftround']]

# Replace NaN values with empty strings
df_selected.fillna('', inplace=True)

# Save the modified DataFrame to a new CSV file
df_selected.to_csv('players_edited.csv', index=False)

print(f"Successfully created players_edited.csv with {len(df_selected)} records")