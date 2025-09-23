import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.agenda_planner.agenda_planner import generate_agenda
import json

# Example input (UI would send this)
user_input = {
    "topics": [
        "Social Media Campaign Review",
        "Q4 Advertising Budget"
    ],
    "discussion_points": [
        "Analyze recent email marketing performance",
        "Plan upcoming influencer collaborations",
        "Evaluate content strategy effectiveness"
    ],
    "date": "2025-09-10"
}


agenda = generate_agenda(user_input)

# Print nicely formatted JSON
print(json.dumps(agenda, indent=4))
