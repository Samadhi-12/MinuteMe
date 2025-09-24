# backend/agents/minutes_generator/minutes_generator.py

from datetime import datetime, timedelta
import re

def generate_minutes(transcript_text: str) -> dict:
    """
    Comprehensive minutes generator:
    - Extracts discussion_points, decisions, action_items
    - Extracts current discussion, future discussion, next meeting date
    """
    lines = transcript_text.splitlines()

    # Core categories
    discussion_points = []
    decisions = []
    action_items = []

    # Advanced categories
    current_discussion = []
    future_discussion = []
    next_meeting_date = None

    # Regex to find dates (dd/mm/yyyy or yyyy-mm-dd)
    date_patterns = [
        r"(\d{1,2}/\d{1,2}/\d{2,4})",
        r"(\d{4}-\d{1,2}-\d{1,2})"
    ]

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        lower_line = stripped.lower()

        # ----- Core categories -----
        if lower_line.startswith("decision:"):
            decisions.append(stripped[len("decision:"):].strip())
        elif lower_line.startswith("action:"):
            action_items.append(stripped[len("action:"):].strip())
        else:
            discussion_points.append(stripped)

        # ----- Advanced categories -----
        if any(keyword in lower_line for keyword in ["will discuss", "to be discussed", "for next meeting", "agenda"]):
            future_discussion.append(stripped)
        elif "next meeting" in lower_line:
            future_discussion.append(stripped)
            # Try to extract date
            for pattern in date_patterns:
                match = re.search(pattern, stripped)
                if match:
                    for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
                        try:
                            next_meeting_date = datetime.strptime(match.group(0), fmt)
                            break
                        except ValueError:
                            continue
        else:
            current_discussion.append(stripped)

    # Default next meeting date if not found
    if next_meeting_date is None:
        next_meeting_date = datetime.now() + timedelta(days=7)

    minutes_doc = {
        # Core
        "discussion_points": discussion_points,
        "decisions": decisions,
        "action_items": action_items,
        # Advanced
        "current_discussion": current_discussion,
        "future_discussion": future_discussion,
        "next_meeting_date": next_meeting_date.strftime("%Y-%m-%d")
    }

    return minutes_doc
