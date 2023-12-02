# Project: Adaptive Task Scheduler for Social and Intelligent Assistive Robots in Home Environment

## Overview
This project, developed by Priyank Avijeet and Vinayak Gajendra Panchal, focuses on integrating Social and Intelligent Assistive Robots into the home automation landscape. The core objective is to enhance task scheduling in a way that mirrors human behavior in prioritizing daily activities based on various factors such as emotional context, health sensitivity, and urgency. The system employs advanced Natural Language Processing (NLP) and Transformer models, along with a self-adaptive software architecture using the MAPEK loop, to dynamically adjust task prioritization.

## Repository Structure


code/
│
├── adapt_emotion_weights.py # Script for adjusting emotion preference weights
├── app.py # Main application script
├── data/ # Directory containing data files
│   ├── commands.csv # CSV file with user commands
│   ├── commands.json # JSON file with user commands
│   ├── emotion_weights.json # JSON file with emotion weights data
│   └── emotional_state.json # JSON file with emotional state data
├── health_text_classification.py # Script for health-related text classification
├── libs.py # Library functions used across the project
├── sentiment_analyser.py # Script for sentiment analysis
├── static/ # Static files for the web interface
│   ├── robot_image_happy.png # Image of robot in a happy state
│   ├── robot_image_neutral.png # Image of robot in a neutral state
│   └── robot_image_sad.png # Image of robot in a sad state
├── templates/ # HTML templates for the web interface
│   └── index.html # Main HTML template
└── update_emotional_state.py # Script for updating the robot's emotional state


## Key Features
- **Task Scheduling**: Prioritizes tasks based on a unique algorithm considering emotional context, health sensitivity, and temporal aspects.
- **NLP and Transformer Models**: Extracts and interprets task-related information from user inputs.
- **Self-Adaptive Software Architecture**: Utilizes the MAPE-K loop for dynamic adjustment of task prioritization.
- **Emotional Intelligence**: Adjusts emotion preference weights based on user input trends.
- **Graphical User Interface**: Visualizes the robot’s task stack and its current emotional state.

## Setup and Installation
1. Ensure Python 3.11 is installed on your system.
2. Clone the repository to your local machine.
4. Run `app.py` to start the application.

## Usage
- Start the application using the command `python app.py`.
- Interact with the system through the provided Graphical User Interface via a web browser.
- Input tasks and observe how the system schedules and prioritizes them.

## Authors
- Priyank Avijeet
- Vinayak Gajendra Panchal


## Acknowledgments
We express our sincere gratitude to Professor Ladan Tahvildari and our teaching assistants, Mingyang Xu and Ryan Zheng He Liu, for their invaluable guidance throughout our course. Our thanks also extend to the IBM team for providing resources that were crucial in applying our skills to realworld
systems and enhancing our understanding of MAPEK based self-adaptive software systems. The assignments and quizzes significantly aided in translating theoretical knowledge into practical solutions, and we are deeply appreciative of the support and opportunities offered by our instructors, which
have been instrumental in our academic growth.


