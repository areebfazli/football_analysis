import pandas as pd

def get_player_data():
    """
    Retrieves and displays a summarized, human-readable report of a player's career data.
    """
    player_name = input("Enter the player's name: ")
    try:
        # Load all CSV files into pandas DataFrames
        data_path = 'player_scores/'
        appearances_df = pd.read_csv(data_path + 'appearances.csv')
        clubs_df = pd.read_csv(data_path + 'clubs.csv')
        game_lineups_df = pd.read_csv(data_path + 'game_lineups.csv')
        player_valuations_df = pd.read_csv(data_path + 'player_valuations.csv')
        players_df = pd.read_csv(data_path + 'players.csv')
        transfers_df = pd.read_csv(data_path + 'transfers.csv')

        # Find the player by name (case-insensitive)
        player = players_df[players_df['name'].str.lower() == player_name.lower()]
        if player.empty:
            print(f"Player '{player_name}' not found.")
            return

        player_info = player.iloc[0]
        player_id = player_info['player_id']
        print(f"\n--- Player Summary for {player_info['name']} (ID: {player_id}) ---\n")

        # --- Personal Information ---
        print("Personal Information:")
        print(f"  - Country: {player_info['country_of_citizenship']}")
        print(f"  - Date of Birth: {player_info['date_of_birth']}")
        print(f"  - Position: {player_info['position']}")
        print(f"  - Foot: {player_info['foot']}")
        print(f"  - Height: {player_info['height_in_cm']} cm\n")

        # --- Career Summary ---
        print("Career Summary:")
        player_appearances = appearances_df[appearances_df['player_id'] == player_id]
        total_goals = int(player_appearances['goals'].sum())
        total_assists = int(player_appearances['assists'].sum())
        total_minutes = int(player_appearances['minutes_played'].sum())
        print(f"  - Total Appearances: {len(player_appearances)}")
        print(f"  - Total Goals: {total_goals}")
        print(f"  - Total Assists: {total_assists}")
        print(f"  - Total Minutes Played: {total_minutes}\n")

        # --- Performance by Club ---
        print("Performance by Club:")
        player_lineups = game_lineups_df[game_lineups_df['player_id'] == player_id]
        if not player_appearances.empty and not player_lineups.empty:
            player_appearances_with_club = player_appearances.merge(
                player_lineups[['game_id', 'club_id']], on='game_id'
            )
            player_appearances_with_club = player_appearances_with_club.merge(
                clubs_df[['club_id', 'name']], on='club_id'
            )
            club_stats = player_appearances_with_club.groupby('name').agg(
                appearances=('game_id', 'count'),
                goals=('goals', 'sum'),
                assists=('assists', 'sum'),
                minutes_played=('minutes_played', 'sum')
            ).astype(int)

            if not club_stats.empty:
                print(club_stats.to_string())
            else:
                print("  - No detailed club performance data available.")
        else:
            print("  - No detailed club performance data available.")
        print("\n")


        # --- Valuation History ---
        print("Valuation History:")
        player_valuations = player_valuations_df[player_valuations_df['player_id'] == player_id]
        if not player_valuations.empty:
            latest_valuation = player_valuations.sort_values(by='date', ascending=False).iloc[0]
            highest_valuation = player_valuations.loc[player_valuations['market_value_in_eur'].idxmax()]
            print(f"  - Latest Valuation:  €{int(latest_valuation['market_value_in_eur']):,} on {latest_valuation['date']}")
            print(f"  - Highest Valuation: €{int(highest_valuation['market_value_in_eur']):,} on {highest_valuation['date']}\n")
        else:
            print("  - No valuation data available.\n")

        # --- Transfer History ---
        print("Transfer History:")
        player_transfers = transfers_df[transfers_df['player_id'] == player_id].sort_values('transfer_date')
        if not player_transfers.empty:
            # This section seems overly complex and might be the source of errors.
            # The transfers.csv already contains club names. Let's simplify.
            for _, row in player_transfers.iterrows():
                from_club = row['from_club_name']
                to_club = row['to_club_name']
                fee_value = row.get('transfer_fee', 0)
                fee = f"for €{int(fee_value):,}" if pd.notna(fee_value) and fee_value > 0 else "on a free transfer"
                
                # The logic here can be simplified by just stating the transfer details directly
                print(f"  - Transfer from {from_club} to {to_club} on {row['transfer_date']} {fee}.")
        else:
            print("  - No transfer data available.")

    except FileNotFoundError as e:
        print(f"Error: {e}. Make sure the 'player_scores' directory and its CSV files are in the correct path.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    get_player_data()
