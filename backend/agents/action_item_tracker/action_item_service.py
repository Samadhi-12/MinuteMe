import json
import os
from datetime import datetime
from lib.database import update_minutes_with_action_items

def save_action_items(minutes_id: str, action_items: list):
    """
    Updates a minutes document in MongoDB with the extracted action items.
    
    Args:
        minutes_id (str): The MongoDB document _id for the minutes.
        action_items (list): The list of action items to save.
    """
    if not minutes_id:
        print("⚠️ Cannot save action items: minutes_id is missing.")
        return None
    
    modified_count = update_minutes_with_action_items(minutes_id, action_items)
    return modified_count