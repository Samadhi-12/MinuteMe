import json
import os

def read_agenda(meeting_id: str):
    agenda_path = os.path.join('data', 'agendas', f'{meeting_id}.json')
    try:
        with open(agenda_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None