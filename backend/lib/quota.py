from datetime import datetime
from bson.objectid import ObjectId
from .database import get_db

def get_monthly_meeting_count(user_id: str) -> int:
    """Counts meetings created by a user in the current month."""
    db = get_db()
    
    # Get the first day of the current month
    now = datetime.now()
    first_day = datetime(now.year, now.month, 1)
    
    # Find all meetings created by the user this month
    count = db.meetings.count_documents({
        "user_id": user_id,
        "created_at": {"$gte": first_day}
    })
    return count

def get_monthly_automation_cycles(user_id: str) -> int:
    """Counts automated processing cycles used by a user in the current month."""
    db = get_db()
    
    # Get the first day of the current month
    now = datetime.now()
    first_day = datetime(now.year, now.month, 1)
    
    # Count documents where automation was used
    count = db.meetings.count_documents({
        "user_id": user_id,
        "created_at": {"$gte": first_day},
        "automation_used": True
    })
    return count

def increment_automation_cycle(meeting_id: str, user_id: str) -> bool:
    """Marks a meeting as having used an automation cycle."""
    db = get_db()
    result = db.meetings.update_one(
        {"_id": ObjectId(meeting_id), "user_id": user_id},
        {"$set": {"automation_used": True}}
    )
    return result.modified_count > 0

def check_free_tier_limits(user_id: str, action_type: str = "meeting"):
    """
    Checks if a free tier user has exceeded their limits.
    
    Args:
        user_id: The user ID to check
        action_type: The type of action being performed ("meeting", "transcription", "automation")
        
    Returns:
        tuple: (exceeded_limit, limit_info)
    """
    if action_type == "meeting":
        limit = 5
        current = get_monthly_meeting_count(user_id)
        return (current >= limit, {"limit": limit, "used": current, "remaining": max(0, limit - current)})
    
    elif action_type == "automation":
        limit = 5
        current = get_monthly_automation_cycles(user_id)
        return (current >= limit, {"limit": limit, "used": current, "remaining": max(0, limit - current)})
    
    elif action_type == "transcription":
        limit = 5
        current = get_monthly_transcription_count(user_id)
        return (current >= limit, {"limit": limit, "used": current, "remaining": max(0, limit - current)})
    
    return (False, {})

def get_monthly_transcription_count(user_id: str) -> int:
    """
    Counts automated transcription operations performed by a user in the current month.
    """
    db = get_db()
    
    # Get the first day of the current month
    now = datetime.now()
    first_day = datetime(now.year, now.month, 1)
    
    # Count documents where automated transcription was used
    count = db.transcripts.count_documents({
        "user_id": user_id,
        "created_at": {"$gte": first_day},
        "automated": True  # Only count automated transcriptions
    })
    return count