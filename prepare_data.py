
import pandas as pd
from datetime import datetime

def prepare_player_data():
    """
    Loads player, appearance, and game data, then engineers features to create a
    clean dataset for market value prediction.
    """
    # Load the datasets
    try:
        players = pd.read_csv('/home/areeb/football/player_scores/players.csv')
        appearances = pd.read_csv('/home/areeb/football/player_scores/appearances.csv')
        games = pd.read_csv('/home/areeb/football/player_scores/games.csv')
    except FileNotFoundError as e:
        print(f"Error loading data: {e}. Make sure the CSV files are in the 'player_scores' directory.")
        return

    # 1. Feature Engineering on players data
    # Calculate age
    def calculate_age(born):
        if pd.isnull(born):
            return None
        today = datetime.today()
        return today.year - datetime.strptime(born, '%Y-%m-%d %H:%M:%S').year

    players['age'] = players['date_of_birth'].apply(calculate_age)

    # Select relevant player columns
    players_cleaned = players[[
        'player_id',
        'market_value_in_eur',
        'position',
        'foot',
        'height_in_cm',
        'age'
    ]].copy()

    # 2. Aggregate performance stats from appearances
    performance_stats = appearances.groupby('player_id').agg(
        total_goals=('goals', 'sum'),
        total_assists=('assists', 'sum'),
        total_minutes_played=('minutes_played', 'sum')
    ).reset_index()

    # 3. Merge datasets
    # Merge players with their performance stats
    merged_data = pd.merge(players_cleaned, performance_stats, on='player_id', how='left')

    # 4. Clean the final dataset
    # Drop rows where market value is missing, as it's our target variable
    merged_data.dropna(subset=['market_value_in_eur'], inplace=True)

    # Fill missing values for features
    merged_data['age'].fillna(merged_data['age'].median(), inplace=True)
    merged_data['height_in_cm'].fillna(merged_data['height_in_cm'].median(), inplace=True)
    merged_data['foot'].fillna('Unknown', inplace=True)
    merged_data.fillna({
        'total_goals': 0,
        'total_assists': 0,
        'total_minutes_played': 0
    }, inplace=True)

    # Save the final dataset
    output_path = '/home/areeb/football/player_market_value_data.csv'
    merged_data.to_csv(output_path, index=False)
    print(f"Data successfully prepared and saved to {output_path}")

if __name__ == '__main__':
    prepare_player_data()
