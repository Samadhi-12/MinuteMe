from utils import (
    save_json,
    get_next_meeting_id,
    extract_keywords_rake,
    get_user_input_if_no_previous_file,
    save_text,
)
from datetime import datetime

def assign_priority(topic):
    """Assign priority based on keywords in topic"""
    topic_lower = topic.lower()
    if any(word in topic_lower for word in ["deploy", "bug", "critical", "urgent"]):
        return "urgent"
    elif any(word in topic_lower for word in ["plan", "roadmap", "strategy", "design", "budget"]):
        return "discussion"
    else:
        return "info"

def allocate_time(priority):
    """Allocate time based on priority"""
    if priority == "urgent":
        return "20 mins"
    elif priority == "discussion":
        return "15 mins"
    return "10 mins"

def generate_meeting_summary(meeting_name, agenda_items):
    """Create a concise textual summary for the meeting."""
    lines = []
    lines.append(f"Meeting: {meeting_name}")
    lines.append("Summary:")
    counts = {"urgent": 0, "discussion": 0, "info": 0}
    for item in agenda_items:
        pr = item.get("priority", "info")
        if pr in counts:
            counts[pr] += 1
    lines.append(
        f"- Topics: {len(agenda_items)} (urgent: {counts['urgent']}, discussion: {counts['discussion']}, info: {counts['info']})"
    )
    lines.append("Key Items:")
    for item in agenda_items[:5]:
        lines.append(f"- {item['topic']} [{item['priority']}] - {item['time_allocated']}")
    return "\n".join(lines)

def generate_agenda(user_input=None):
    """
    Generate structured agenda JSON.
    If user_input is None, it will automatically grab from previous meeting file
    or fallback to default example.
    """

    # 0️⃣ Grab user input if not provided
    if user_input is None:
        user_input = get_user_input_if_no_previous_file()

    # 1️⃣ Create meeting ID
    meeting_id = get_next_meeting_id()

    # 2️⃣ Combine all topics
    all_topics = user_input.get("topics", []) + user_input.get("discussion_points", [])

    # 3️⃣ Generate short agenda topics using RAKE
    agenda_items = []
    for topic in all_topics:
        # RAKE returns list of phrases, safe to call .title()
        short_topics = extract_keywords_rake(topic, top_n=1) or [topic]
        short_topic = short_topics[0].title()

        priority = assign_priority(topic)
        time_alloc = allocate_time(priority)

        agenda_items.append({
            "topic": short_topic,
            "priority": priority,
            "time_allocated": time_alloc
        })

    # 4️⃣ Generate meeting name from top keywords (RAKE)
    top_keywords = extract_keywords_rake(" ".join(all_topics), top_n=5)
    meeting_name = " ".join([kw.title() for kw in top_keywords]) or "General Meeting"

    # 5️⃣ Build final agenda JSON
    agenda_json = {
        "meeting_id": meeting_id,
        "meeting_name": meeting_name,
        "meeting_date": user_input.get("date") or str(datetime.today().date()),
        "agenda": agenda_items
    }

    # 6️⃣ Ensure per-meeting folder and save summary + JSON inside it
    meeting_dir = f"backend/data/agendas/{meeting_id}"
    summary_text = generate_meeting_summary(meeting_name, agenda_items)
    save_text(summary_text, f"{meeting_dir}/summary.txt")
    agenda_json["summary"] = summary_text
    save_json(agenda_json, f"{meeting_dir}/agenda.json")

    return agenda_json


# ✅ Optional: allow running independently for testing
if __name__ == "__main__":
    agenda = generate_agenda()
    import json
    print("✅ Agenda created:")
    print(json.dumps(agenda, indent=4))
