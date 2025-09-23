from agents.agenda_planner.agenda_planner import generate_agenda
from agents.minutes_generator.generator import generate_minutes
from agents.action_item_tracker.tracker import extract_and_schedule_tasks

# Dummy meeting info for testing
meeting_info = {
    "title": "Project Sync",
    "attendees": ["John", "Sarah", "Alex"],
    "date": "2025-09-06"
}

# Dummy transcript
transcript = """
John will prepare the budget report by Friday.
Sarah will update the project plan.
The team should review the design next week.
"""

# Simple function to check if task is done
def task_done(task):
    return False

# Step 1: Prepare Agenda
agenda = generate_agenda(meeting_info)
print("Agenda JSON:")
print(agenda)

# Step 2: Generate Minutes (simulate)
minutes = generate_minutes(transcript)

# Step 3: Extract Action Items
action_items = extract_and_schedule_tasks(minutes)
print("Action Items JSON:")
print(action_items)

# Step 4: Add unfinished tasks to next agenda
agenda["follow_ups"] = [task for task in action_items["action_items"] if not task_done(task)]
print("Agenda with follow-ups:")
print(agenda)
