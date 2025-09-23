from agents.action_item_tracker.tracker import result
from agents.action_item_tracker.calendar_service import schedule_action_item


for item in result['action_items']:
    task = item.get('task')
    owner = item.get('owner')
    deadline = item.get('deadline')
    description = f"Action item assigned to {owner}"
    schedule_action_item(task, description, deadline, owner)
