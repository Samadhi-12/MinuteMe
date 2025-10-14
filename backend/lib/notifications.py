from datetime import datetime
from bson.objectid import ObjectId
from .database import get_db
import os

def create_notification(user_id: str, message: str, type: str = "info", related_id: str = None) -> str:
    """Creates a notification for a user and returns its ID."""
    db = get_db()
    notification = {
        "user_id": user_id,
        "message": message,
        "type": type,
        "related_id": related_id,
        "read": False,
        "created_at": datetime.utcnow(),
        "email_delivered": False
    }
    result = db.notifications.insert_one(notification)
    return str(result.inserted_id)

def get_user_notifications(user_id: str, limit: int = 20) -> list:
    """Gets recent notifications for a user."""
    db = get_db()
    notifications = list(db.notifications.find(
        {"user_id": user_id},
        sort=[("created_at", -1)],
        limit=limit
    ))
    
    for notification in notifications:
        if "_id" in notification:
            notification["id"] = str(notification["_id"])
            del notification["_id"]
    
    return notifications

def mark_notification_read(notification_id: str, user_id: str) -> bool:
    """Marks a notification as read."""
    db = get_db()
    result = db.notifications.update_one(
        {"_id": ObjectId(notification_id), "user_id": user_id},
        {"$set": {"read": True}}
    )
    return result.modified_count > 0

def mark_all_notifications_read(user_id: str) -> int:
    """Marks all notifications as read for a user."""
    db = get_db()
    result = db.notifications.update_many(
        {"user_id": user_id, "read": False},
        {"$set": {"read": True}}
    )
    return result.modified_count

def update_notification_email_status(notification_id: str, delivered: bool) -> bool:
    """Updates the email delivery status of a notification."""
    db = get_db()
    result = db.notifications.update_one(
        {"_id": ObjectId(notification_id)},
        {"$set": {"email_delivered": delivered}}
    )
    return result.modified_count > 0

def send_email_notification(user_id: str, subject: str, message: str) -> bool:
    """
    Sends an email notification to a user.
    For now, this is a placeholder - implement with your chosen email service.
    """
    try:
        from clerk_backend_api import Clerk
        
        # Get user email from Clerk
        clerk = Clerk(bearer_auth=os.getenv("CLERK_SECRET_KEY"))
        user = clerk.users.get(user_id)
        
        if user and user.email_addresses:
            email = user.email_addresses[0].email_address
            
            # Here you would integrate with an email service like SendGrid, Mailgun, etc.
            # For now, we'll just log it
            print(f"🔔 WOULD SEND EMAIL: To {email}, Subject: {subject}, Message: {message}")
            return True
    except Exception as e:
        print(f"Failed to send email notification: {e}")
    
    return False