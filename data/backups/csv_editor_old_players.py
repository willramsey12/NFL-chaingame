import pandas as pd

# Load CSV file with specific column handling
df = pd.read_csv('players_old.csv', dtype=str)

# Select relevant columns and match with previous structure
df_selected = df[['name', 'first_name', 'last_name', 'birth_date', 'college',
                  'position', 'height', 'weight', 'draft_team', 'draft_round']]

# Rename columns to match previous structure
df_selected.rename(columns={
    'name': 'display_name',
    'college': 'college_name',
    'draft_team': 'draft_club',
    'draft_round': 'draftround'
}, inplace=True)

# Add empty placeholders for missing columns
df_selected['jersey_number'] = ''
df_selected['team_abbr'] = ''
df_selected['headshot'] = ''

# Reorder columns to match exactly
df_selected = df_selected[['display_name', 'first_name', 'last_name', 'birth_date', 'college_name',
                           'position', 'jersey_number', 'height', 'weight', 'team_abbr',
                           'draft_club', 'headshot', 'draftround']]

# Replace NaN values with empty strings
df_selected.fillna('', inplace=True)

# Save the modified DataFrame to a new CSV file
df_selected.to_csv('old_players_edited.csv', index=False)

print(f"Successfully created players_edited.csv with {len(df_selected)} records")
