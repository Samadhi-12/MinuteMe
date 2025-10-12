import json
import os
from datetime import datetime

def save_action_items(meeting_id: str, action_items: list):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"action_items_{meeting_id}_{timestamp}.json"
    folder = os.path.join('data', 'action_items')
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)
    with open(filepath, 'w') as f:
        json.dump({
            "meeting_id": meeting_id,
            "timestamp": timestamp,
            "items": action_items
        }, f, indent=2)
    return filepath