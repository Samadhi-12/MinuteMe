import os
from .ai_providers import gemini_provider
from .calendar_service import schedule_action_item

def run_action_item_tracker(meeting_text: str):
    return {
        "provider": "Gemini",
        "action_items": gemini_provider.extract_action_items(meeting_text)
    }

def extract_and_schedule_tasks(meeting_text: str, schedule=True):
    """This is the function coordinator/api will call"""
    result = run_action_item_tracker(meeting_text)

    if schedule:
        for item in result['action_items']:
            task = item.get('task')
            owner = item.get('owner')
            deadline = item.get('deadline')
            description = f"Action item assigned to {owner}"
            schedule_action_item(task, description, deadline, owner)
    return result

# ✅ Only run this when executing the script directly
if __name__ == "__main__":
    sample_notes = """
    John will prepare the budget report by Friday.
    Sarah will update the project plan.
    The team should review the design next week.
    """
    action_items = extract_and_schedule_tasks(sample_notes)
    print(action_items)
