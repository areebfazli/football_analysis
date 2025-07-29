
import pandas as pd
import json

def custom_encode_categorical_data():
    """
    Loads player data, applies a custom numerical encoding for 'position' and
    'foot' columns, saves the mappings to a JSON file, and saves the result
    to a new CSV file.
    """
    # Load the dataset
    try:
        df = pd.read_csv('player_data_final.csv')
    except FileNotFoundError:
        print("Error: 'player_market_value_data.csv' not found.")
        print("Please run the 'prepare_data.py' script first to generate it.")
        return

    # Make a copy to avoid changing the original dataframe
    df_encoded = df.copy()

    # 1. Define the custom mappings
    position_mapping = {
        'Missing': 0,
        'Goalkeeper': 1,
        'Defender': 2,
        'Midfield': 3,
        'Attack': 4
    }

    foot_mapping = {
        'right': 0,
        'left': 1,
        'both': 2,
        'Unknown': 3
    }

    # 2. Apply the custom mappings to the columns
    df_encoded['position'] = df_encoded['position'].map(position_mapping)
    df_encoded['foot'] = df_encoded['foot'].map(foot_mapping)

    print("Applied custom encoding...")
    print("\n'position' column encoded with:")
    print(position_mapping)
    print("\n'foot' column encoded with:")
    print(foot_mapping)

    # 3. Save the mappings to a JSON file
    all_mappings = {
        'position': position_mapping,
        'foot': foot_mapping
    }
    mappings_path = 'encoding_mappings.json'
    with open(mappings_path, 'w') as f:
        json.dump(all_mappings, f, indent=4)
    print(f"\nEncoding mappings saved to '{mappings_path}'")

    # 4. Save the encoded dataset to a new file
    output_path = 'player_data_encoded.csv'
    df_encoded.to_csv(output_path, index=False)
    print(f"Encoded data successfully saved to '{output_path}'")

if __name__ == '__main__':
    custom_encode_categorical_data()
