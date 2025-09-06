import os
from ai_providers import gemini_provider

def run_action_item_tracker(meeting_text: str):
    return {
        "provider": "Gemini",
        "action_items": gemini_provider.extract_action_items(meeting_text)
    }

if __name__ == "__main__":
    sample_notes = """
    John will prepare the budget report by Friday.
    Sarah will update the project plan.
    The team should review the design next week.
    """
    result = run_action_item_tracker(sample_notes)
    print(result)
