import os
import json

def read_previous_minutes():
    minutes_path = os.path.join('backend', 'data', 'previous_meeting', 'meeting_details.json')
    try:
        with open(minutes_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None