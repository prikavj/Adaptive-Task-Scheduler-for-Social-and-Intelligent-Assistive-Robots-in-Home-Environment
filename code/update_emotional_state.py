import pandas as pd
from datetime import datetime, timedelta
import json
import schedule
import time

def process_emotional_state():
    # Load the CSV file
    file_path = './data/commands.csv'
    df = pd.read_csv(file_path)

    # Convert the 'timestamp' column from string to datetime objects
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y-%m-%d %H:%M:%S')

    # Filter out entries from the last 8 hours
    now = datetime.now()
    eight_hours_ago = now - timedelta(hours=8)
    recent_df = df[df['timestamp'] >= eight_hours_ago]

    # Calculate the average scores for each emotion
    average_scores = recent_df[['happy', 'neutral', 'sad']].mean().fillna(0)

    print("Priyank ----------")
    print(average_scores)
    # Determine the current emotion based on the highest score
    current_emotion = average_scores.idxmax()
    print(current_emotion)
    # Save the emotional state to a JSON file
    emotional_state = {"current_emotion": current_emotion}
    json_file_path = './data/emotional_state.json'
    with open(json_file_path, 'w') as json_file:
        json.dump(emotional_state, json_file)

# Schedule the task
schedule.every(10).seconds.do(process_emotional_state)

def main():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
