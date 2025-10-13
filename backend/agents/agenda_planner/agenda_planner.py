from .utils import (
    save_json,
    get_next_meeting_id,
    extract_keywords_rake,
    get_user_input_if_no_previous_file,
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

def generate_agenda(user_input=None):
    """
    Generate structured agenda JSON.
    If user_input is None, it will automatically grab from previous meeting file
    or fallback to default example.
    """
    print("\n--- 🚀 Starting Agenda Planner ---")

    # If called with no user_input, try to load the latest agenda from disk
    if user_input is None:
        import os, json
        agenda_dir = "data/agendas"
        if os.path.exists(agenda_dir):
            files = [f for f in os.listdir(agenda_dir) if f.endswith('.json')]
            if files:
                # Get the latest agenda file by meetingId number
                files.sort(reverse=True)
                latest_file = os.path.join(agenda_dir, files[0])
                print(f"📖 No input provided. Loading latest agenda: {files[0]}")
                with open(latest_file, "r") as f:
                    return json.load(f)
        # If no agenda exists, fallback to default
        print("⚠️ No input or existing agendas found. Using default example.")
        user_input = get_user_input_if_no_previous_file()
    else:
        print("🧠 Using provided input to generate new agenda.")

    # 1️⃣ Create meeting ID
    meeting_id = get_next_meeting_id()

    # 2️⃣ Combine all topics
    all_topics = user_input.get("topics", []) + user_input.get("discussion_points", [])

    # 3️⃣ Generate short agenda topics using RAKE
    agenda_items = []
    for topic in all_topics:
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

    # 6️⃣ Save JSON
    output_path = f"data/agendas/{meeting_id}.json"
    save_json(agenda_json, output_path)
    print(f"✅ Agenda created and saved to: {output_path}")
    print("--- ✨ Finished Agenda Planner ---\n")

    return agenda_json


# ✅ Optional: allow running independently for testing
if __name__ == "__main__":
    agenda = generate_agenda()
    import json
    print("✅ Agenda created:")
    print(json.dumps(agenda, indent=4))
