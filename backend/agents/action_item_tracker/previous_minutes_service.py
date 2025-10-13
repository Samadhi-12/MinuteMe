import os
import json
from lib.database import get_latest_minutes

def read_previous_minutes(user_id: str = "user_placeholder_123"):
    """
    Reads the most recent meeting minutes for a given user from MongoDB.
    
    Args:
        user_id (str): The ID of the user (from Clerk). Placeholder for now.
    """
    print(f"📖 Reading previous minutes from MongoDB for user: {user_id}")
    minutes = get_latest_minutes(user_id)
    if not minutes:
        print(f"⚠️ No previous minutes found in MongoDB for user: {user_id}")
    return minutes