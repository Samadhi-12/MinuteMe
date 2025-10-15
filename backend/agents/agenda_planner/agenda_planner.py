from .utils import (
    get_next_meeting_id,
    extract_keywords_rake,
    get_user_input_if_no_previous_file,
)
from lib.database import save_agenda  # Import the new DB function
from datetime import datetime
from transformers import pipeline

# 🧠 Initialize the AI model once to be reused.
# This prevents reloading the large model on every function call.
priority_classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")


def assign_priority(topic):
    """
    Assign priority based on the semantic meaning of the topic using an AI model.
    """
    print(f"🤖 Analyzing topic for priority: '{topic}'")
    candidate_labels = ["urgent issue", "strategic discussion", "general information"]
    
    # The model predicts which label best fits the topic
    result = priority_classifier(topic, candidate_labels)
    
    # Get the label with the highest score
    top_label = result['labels'][0]

    # Map the detailed AI prediction back to your simple categories
    if "urgent" in top_label:
        return "urgent"
    elif "discussion" in top_label:
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


def generate_agenda(user_input=None, user_id="user_placeholder_123"):
    """
    Generate structured agenda JSON.
    If user_input is None, it will automatically grab from previous meeting file
    or fallback to default example.
    """
    print("\n--- 🚀 Starting Agenda Planner ---")

    # If called with no user_input, try to load from previous minutes in DB
    if user_input is None:
        print("🧠 No input provided. Checking DB for previous meeting minutes.")
        user_input = get_user_input_if_no_previous_file(user_id)
    else:
        print("🧠 Using provided input to generate new agenda.")

    # 1️⃣ Create meeting ID
    meeting_id = get_next_meeting_id(user_id)

    # 2️⃣ Combine all topics
    all_topics = user_input.get("topics", []) + user_input.get("discussion_points", [])

    # 3️⃣ Generate short agenda topics using RAKE
    agenda_items = []
    for topic in all_topics:
        short_topics = extract_keywords_rake(topic, top_n=1) or [topic]
        short_topic = short_topics[0].title()

        priority = assign_priority(topic) # ✨ This now uses the AI model
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

    # 6️⃣ Save to MongoDB and get the serializable result
    saved_agenda = save_agenda(agenda_json, user_id)
    print(f"✅ Agenda '{meeting_id}' saved to MongoDB for user '{user_id}'.")
    print("--- ✨ Finished Agenda Planner ---\n")

    return saved_agenda


# ✅ Optional: allow running independently for testing
if __name__ == "__main__":
    # Example input to see the AI in action
    mock_input = {
        "topics": [
            "The production server is down and needs immediate attention.",
            "Reviewing the financial projections for the next quarter.",
            "Let's go over the designs for the new user dashboard.",
            "Quick update on the team's holiday leave schedule."
        ],
        "discussion_points": []
    }
    agenda = generate_agenda(user_input=mock_input)
    import json
    print("✅ Agenda created:")
    print(json.dumps(agenda, indent=4))