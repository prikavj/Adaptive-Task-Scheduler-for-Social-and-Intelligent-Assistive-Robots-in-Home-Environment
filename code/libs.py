import os
import json
import random
from datetime import datetime, timedelta
from sentiment_analyser import emotion_score
from health_text_classification import health_text_classifier
import re
import spacy
import csv

# Load the language model
nlp = spacy.load("en_core_web_sm")

# List of emotion names
emotion_names = ['happy', 'neutral', 'sad']

def update_command_priorities():
    print("Update Command Priorities called.")
    # Read the current commands data from the file
    with open('./data/commands.json', 'r', encoding='utf-8') as f:
        commands = json.load(f)
    
    with open('./data/emotion_weights.json', 'r') as file:
        emotion_weights = json.load(file)


    
    # Update the priorities for the commands
    for command in commands['commands']:
        print(command)
        if 'priority' in command and command['priority'] not in [0, 0.99, 1]:
                print("Came here!")
                emotion_scores = {
                    'happy' : command['happy'],
                    'sad' : command['sad'],
                    'neutral' : command['neutral'],
                }


                # Calculate the weighted score for each emotion and sum them up
                total_emotion_score = 0
                for emotion, score in emotion_scores.items():
                    weight = emotion_weights.get(emotion, 0)  # Default weight is 0 if not found
                    total_emotion_score += score * (weight / 100)
                health_emergency_score = command['health_emergency_score']
                health_sensitivity_score = command['health_sensitivity_score'] 
                # Utility function calculation
                command['priority'] = 0.65 * total_emotion_score + 0.35 * health_sensitivity_score
                if health_emergency_score > 0.30:
                    command['priority'] = 1
    
    # Write the updated data back to the file
    with open('./data/commands.json', 'w', encoding='utf-8') as f:
        json.dump(commands, f, ensure_ascii=False, indent=4)

def get_priority(text):
    # Get emotion scores from the sentiment_analyser.py
    emotion_scores = emotion_score(text)
    
    health_info_dict = health_text_classifier(text)

    print("-------------------------")
    print(emotion_scores)
    print(health_info_dict)
    print("-------------------------") 
    # Load emotion weights from the JSON file
    with open('./data/emotion_weights.json', 'r') as file:
        emotion_weights = json.load(file)

    # Calculate the weighted score for each emotion and sum them up
    total_emotion_score = 0
    for emotion, score in emotion_scores.items():
        weight = emotion_weights.get(emotion, 0)  # Default weight is 0 if not found
        total_emotion_score += score * (weight / 100)
    
    health_emergency_score = health_info_dict['life critical medical emergency']
    health_sensistivity_score = health_info_dict['casual medical need'] 
    # Utility function calculation
    utility_score = 0.65 * total_emotion_score + 0.35 * health_sensistivity_score

    if health_emergency_score > 0.30:
        utility_score = 1

    return utility_score, emotion_scores, health_info_dict

def get_execution_time():
    """
    Generate a random execution time between 25 and 50 seconds.
    """
    return random.randint(25, 50)

def extract_time_info(instruction):
    # Define patterns for different time formats
    time_patterns = {
        'now': r'\bnow\b|\burgently\b',
        'minutes': r'(\d+)\s*(minute|minutes|min|m\b)',
        'hours': r'(\d+)\s*(hour|hours|hrs|h\b)',
        'seconds': r'(\d+)\s*(second|seconds|sec|s\b)',
        'am_pm': r'(\d{1,2})(:\d{2})?\s*(AM|PM)',
    }
    
    current_time = datetime.now()
    
    # Check for each pattern in the instruction
    for key, pattern in time_patterns.items():
        match = re.search(pattern, instruction, re.IGNORECASE)
        if match:
            if key == 'now':
                return 'now'
            elif key in ['minutes', 'hours', 'seconds']:
                number = int(match.group(1))
                if key == 'minutes':
                    return (datetime.now() + timedelta(minutes=number)).isoformat()
                elif key == 'hours':
                    return (datetime.now() + timedelta(hours=number)).isoformat()
                else:
                    return (datetime.now() + timedelta(seconds=number)).isoformat()
            elif key == 'am_pm':
                hour = int(match.group(1))
                minute = int(match.group(2)[1:]) if match.group(2) else 0
                am_pm = match.group(3).upper()
                # Adjust for 12-hour format
                if am_pm == 'PM' and hour < 12:
                    hour += 12
                elif am_pm == 'AM' and hour == 12:
                    hour = 0

                future_time = current_time.replace(hour=hour, minute=minute, second=0, microsecond=0)
                # If the time is in the past, push it to the same time next day
                return future_time.isoformat()  if future_time > current_time else (future_time + timedelta(days=1)).isoformat() 

    # If no time information is found
    return 'none'

def save_to_csv(text, emotion_scores):
    # File path for the CSV file
    csv_file_path = './data/commands.csv'

    # Fields for the CSV
    fieldnames = ['text', 'timestamp'] + emotion_names + ['keywords'] + ['time of the day']

    # Check if the CSV file exists
    file_exists = os.path.isfile(csv_file_path)
    doc = nlp(text)

    # Extract keywords
    keywords = [token.text for token in doc if token.pos_ in ['NOUN'] and not token.is_stop]
    
    """
    Classify the time of the day into morning, afternoon, evening, or night
    based on the hour of the given timestamp.
    """
    timestamp = datetime.now()
    hour = timestamp.hour
    timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")


    if 5 <= hour < 12:
        time_of_day = "morning"
    elif 12 <= hour < 17:
        time_of_day = "afternoon"
    elif 17 <= hour < 21:
        time_of_day = "evening"
    else:
        time_of_day = "night"
    
    # Data to be written
    data = {
        'text': text,  # Update this as per your logic
        'timestamp': timestamp_str,
        'happy' : emotion_scores['happy'],
        'neutral' : emotion_scores['neutral'],
        'sad' : emotion_scores['sad'],
        'keywords': keywords,
        'time of the day' : time_of_day
    }

    # Open the file in append mode ('a')
    with open(csv_file_path, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header only if the file is new
        if not file_exists:
            writer.writeheader()

        # Write the data row
        writer.writerow(data)

def reset():
    file_path = './data/commands.json'

    # Load the existing data from the file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Update the status and execution_time_remaining for all commands
    for command in data["commands"]:
        command["status"] = "waiting"
        command["execution_time_remaining"] = 25

    # Write the updated data back to the file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


def get_emotion_image():
    # Path to the JSON file
    json_file_path = './data/emotional_state.json'

    try:
        # Read the emotional state from the JSON file
        with open(json_file_path, 'r') as file:
            data = json.load(file)
        current_emotion = data.get('current_emotion', 'neutral')  # default to 'neutral' if not found
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading the JSON file: {e}")
        current_emotion = 'neutral'

    # Map emotions to image filenames
    image_files = {
        'happy': 'robot_image_happy.png',
        'sad': 'robot_image_sad.png',
        'neutral': 'robot_image_neutral.png'
    }

    # Select the appropriate image file
    return image_files.get(current_emotion, 'robot_image_neutral.png')