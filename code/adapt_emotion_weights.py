import json
import os
import schedule
import time
from libs import update_command_priorities


def read_json(file_path):
    """Reads and returns data from a JSON file."""
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    else:
        return None

def write_json(file_path, data):
    """Writes data to a JSON file."""
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def update_emotion_weights():
    """Updates the emotion weights based on the current emotional state."""
    emotional_state_path = './data/emotional_state.json'
    emotion_weights_path = './data/emotion_weights.json'

    # Read the current emotional state
    current_emotion_state = read_json(emotional_state_path)
    if current_emotion_state is None:
        print("Emotional state file not found.")
        return

    current_emotion = current_emotion_state.get("current_emotion")

    # Read the current emotion weights
    emotion_weights = read_json(emotion_weights_path)
    if emotion_weights is None:
        print("Emotion weights file not found.")
        return

    # Update weights
    for emotion, value in emotion_weights.items():
        if emotion == current_emotion:
            emotion_weights[emotion] = value + (100 - value) * 0.3
        else:
            emotion_weights[emotion] = value * 0.7

    # Write updated weights back to file
    write_json(emotion_weights_path, emotion_weights)
    print("Emotion weights updated.")
    update_command_priorities()

def main():
    """Schedules the update process to run every hour."""
    schedule.every(10).seconds.do(update_emotion_weights)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
