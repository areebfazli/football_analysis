
import pandas as pd
from datetime import datetime

def update_ages_for_retired_players():
    """
    Identifies retired players based on their last appearance date, calculates
    their age at retirement, and updates this in the final encoded dataset.
    """
    # --- Step 1: Find the last appearance date for each player ---
    try:
        appearances = pd.read_csv('player_scores/appearances.csv')
        players = pd.read_csv('player_scores/players.csv')
        encoded_data = pd.read_csv('player_data_encoded.csv')
    except FileNotFoundError as e:
        print(f"Error loading data: {e}. Please ensure all required CSV files are present.")
        return

    # Convert date columns to datetime objects
    appearances['date'] = pd.to_datetime(appearances['date'])
    players['date_of_birth'] = pd.to_datetime(players['date_of_birth'], errors='coerce')

    # Find the last appearance date for each player
    last_appearance = appearances.groupby('player_id')['date'].max().reset_index()
    last_appearance.rename(columns={'date': 'last_appearance_date'}, inplace=True)

    # --- Step 2: Identify retired players and calculate retirement age ---
    
    # Merge last appearance date with player birth dates
    player_ages = pd.merge(players[['player_id', 'date_of_birth']], last_appearance, on='player_id')

    # Define retired players as those whose last game was before 2023
    retirement_cutoff = datetime(2023, 1, 1)
    player_ages['is_retired'] = player_ages['last_appearance_date'] < retirement_cutoff

    # Calculate age at retirement for retired players
    def calculate_retirement_age(row):
        if row['is_retired'] and pd.notnull(row['date_of_birth']):
            return row['last_appearance_date'].year - row['date_of_birth'].year
        return None

    player_ages['age_at_retirement'] = player_ages.apply(calculate_retirement_age, axis=1)

    # --- Step 3: Update the main dataset with the new ages ---
    
    # Merge the retirement age information into the encoded dataset
    final_data = pd.merge(encoded_data, player_ages[['player_id', 'age_at_retirement']], on='player_id', how='left')

    # Update the 'age' column: if age_at_retirement exists, use it; otherwise, keep the original age
    final_data['age'] = final_data['age_at_retirement'].fillna(final_data['age'])

    # Clean up by dropping the temporary columns
    final_data.drop(columns=['age_at_retirement'], inplace=True)
    
    # Ensure no new NaN values were created in the age column
    final_data['age'] = final_data['age'].fillna(final_data['age'].median())
    final_data['age'] = final_data['age'].astype(int)

    # --- Step 4: Save the final dataset ---
    output_path = 'player_data_final.csv'
    final_data.to_csv(output_path, index=False)

    print("Successfully updated ages for retired players.")
    print(f"The final dataset has been saved to '{output_path}'")

if __name__ == '__main__':
    update_ages_for_retired_players()
