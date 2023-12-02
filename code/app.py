from flask import Flask, render_template, request, jsonify, url_for
import os
from datetime import datetime
from libs import update_command_priorities, get_priority, get_execution_time, extract_time_info, save_to_csv, reset, get_emotion_image
import json


app = Flask(__name__)

@app.route('/')
def index():
    # Select the appropriate image file
    image_file = get_emotion_image()

    # Render the template with the image file
    return render_template('index.html', image_file=image_file)

@app.route('/get_emotion')
def get_emotion():
    
    image_file = get_emotion_image()
    return jsonify(image_file=image_file)


@app.route('/save-text', methods=['POST'])
def save_text():
    if request.method == 'POST':
        data = request.json
        text = data['text']
        execution_time = get_execution_time()
        priority, emotion_scores, health_info_dict =  get_priority(text)
        # Create a dictionary for the new command
        new_command = {
            'command': text,
            'priority': priority,  # Assuming get_priority() is defined
            'status': 'waiting',  # Default status for new commands
            'total_execution_time_needed': execution_time,
            'execution_time_remaining': execution_time,  # Assuming get_execution_time() is defined
            'start_time' : extract_time_info(text),
            'happy' : emotion_scores['happy'],
            'neutral' : emotion_scores['neutral'],
            'sad' : emotion_scores['sad'],
            'health_emergency_score' : health_info_dict['life critical medical emergency'],
            'health_sensitivity_score' : health_info_dict['casual medical need'] 
        }

        # Check if the commands.json file exists
        if not os.path.isfile('./data/commands.json'):
            # Create a new file with the command as the first entry
            commands_data = {'commands': [new_command]}
        else:
            # Read the existing data
            with open('./data/commands.json', 'r', encoding='utf-8') as f:
                commands_data = json.load(f)
            
            # Append the new command to the 'commands' list
            commands_data['commands'].append(new_command)

        # Write the updated data back to the file
        with open('./data/commands.json', 'w', encoding='utf-8') as f:
            json.dump(commands_data, f, ensure_ascii=False, indent=4)
        
        save_to_csv(text, emotion_scores)

        return jsonify(success=True)
    else:
        return 'This route only supports POST requests.', 405

@app.route('/get-commands', methods=['GET'])
def get_commands():
    with open('./data/commands.json', 'r', encoding='utf-8') as f:
        commands = json.load(f)
    return jsonify(commands)

@app.route('/update-task', methods=['POST'])
def update_task():
    current_time = datetime.now()
    with open('./data/commands.json', 'r+', encoding='utf-8') as f:
        data = json.load(f)
        commands = data['commands']  # Get the list of commands

        # Check and update priorities based on start_time
        for command in commands:
            if "start_time" in command:
                start_time_info = command['start_time']
                if start_time_info == 'now': 
                    command['priority'] = 0.99
                
                if start_time_info != 'none' and start_time_info != 'now':
                    start_time_info_formatted =  datetime.fromisoformat(start_time_info)
                    if (isinstance(start_time_info_formatted, datetime) and 0 <= (start_time_info_formatted - current_time).total_seconds() <= 10):
                        command['priority'] = 0.99
                    else:
                        command['priority'] = 0  # Reset priority if not in time range
 

        # Sort commands by priority, highest first, and by remaining time if priorities are equal
        commands.sort(key=lambda x: (-x['priority'], x['execution_time_remaining']))

        # Update the status and execution time of the highest priority task not yet completed
        for command in commands:
            if command['priority'] > 0:
                if command['status'] == 'waiting':
                    command['status'] = 'running'
                    break
                elif command['status'] == 'running':
                    command['execution_time_remaining'] -= 1
                    if command['execution_time_remaining'] <= 0:
                        command['status'] = 'completed'
                    break

        # Update the status and execution time of the highest priority task not yet completed
        running_tasks = [cmd for cmd in commands if cmd['status'] == 'running']
        # Ensure only the highest priority command remains running if multiple were found
        if len(running_tasks) > 1:
            highest_priority_task = running_tasks[0]
            for task in running_tasks[1:]:
                if task != highest_priority_task:
                    task['status'] = 'waiting'

        # Write back the changes to the file
        f.seek(0)
        json.dump(data, f, ensure_ascii=False, indent=4)
        f.truncate()

    return jsonify(success=True)

@app.route('/update-emotion-weights', methods=['POST'])
def update_emotion_weights():
    data = request.json
    # Overwrite the entire file with new data
    with open('./data/emotion_weights.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    update_command_priorities()
    return jsonify(success=True)

@app.route('/get-emotion-weights', methods=['GET'])
def get_emotion_weights():
    with open('./data/emotion_weights.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return jsonify(data)


if __name__ == '__main__':
    reset()
    app.run(debug=True)