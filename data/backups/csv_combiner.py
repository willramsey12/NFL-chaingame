import pandas as pd

# Load both CSV files
df1 = pd.read_csv('players_edited.csv', dtype=str)
df2 = pd.read_csv('old_players_edited.csv', dtype=str)

# Combine both DataFrames directly as their structures match
combined_df = pd.concat([df1, df2], ignore_index=True)

# Remove duplicates based on display_name and birth_date
combined_df.drop_duplicates(subset=['display_name', 'birth_date'], inplace=True)

# Replace NaN values with empty strings
combined_df.fillna('', inplace=True)

# Save the combined DataFrame to a new CSV file
combined_df.to_csv('combined_players.csv', index=False)

print(f"Successfully combined CSV files into combined_players.csv with {len(combined_df)} unique records")
