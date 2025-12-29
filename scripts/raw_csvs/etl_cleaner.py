# scripts/etl_cleaner.py
import pandas as pd
import os

# Define paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(BASE_DIR, "raw_csvs")
OUTPUT_FILE = os.path.join(BASE_DIR, "exercises_clean.json")

def clean_exercise_data():
    csv_path = os.path.join(RAW_DIR, "exercises.csv") # Make sure this file exists
    if not os.path.exists(csv_path):
        print(f"File not found: {csv_path}")
        return

    print("Reading CSV...")
    df = pd.read_csv(csv_path)

    # 1. Basic Cleaning
    df = df.fillna("") # Replace NaNs with empty string
    
    # 2. Rename columns to match your DB model (Adjust these names based on your CSV!)
    # Example: 'Exercise Name' -> 'name'
    # df = df.rename(columns={"Exercise Name": "name", "BodyPart": "muscle_group"})

    # 3. Logic to extract data from URLs (Mock example)
    # If you have a column 'url', you would loop through it here.
    # for index, row in df.iterrows():
    #     url = row['video_url']
    #     # requests.get(url)... extract data...

    # 4. Save to JSON
    print(f"Saving to {OUTPUT_FILE}...")
    df.to_json(OUTPUT_FILE, orient="records", indent=2)
    print("Done!")

if __name__ == "__main__":
    clean_exercise_data()