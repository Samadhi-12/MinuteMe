import json
import os
from lib.database import get_agenda

def read_agenda(meeting_id: str, user_id: str = "user_placeholder_123"):
    """
    Reads a specific agenda for a user from MongoDB.
    """
    print(f"📖 Reading agenda '{meeting_id}' from DB for user: {user_id}")
    agenda = get_agenda(meeting_id, user_id)
    if not agenda:
        print(f"⚠️ Agenda '{meeting_id}' not found in DB.")
    return agenda