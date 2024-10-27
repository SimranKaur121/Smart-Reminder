import json

def load_reminders():
    try:
        with open('data.json', 'r') as f:
            return json.load(f)  # This should return a dictionary
    except FileNotFoundError:
        return {"reminders": []}  # Default structure if the file is not found

def save_reminders(data):
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)
