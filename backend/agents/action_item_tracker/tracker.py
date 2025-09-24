import os
from .ai_providers import gemini_provider
from .calendar_service import schedule_action_item
from .agenda_service import read_agenda
from .action_item_service import save_action_items
import spacy
from datetime import datetime, timedelta
import dateparser

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

def run_action_item_tracker(meeting_text: str):
    return {
        "provider": "Gemini",
        "action_items": gemini_provider.extract_action_items(meeting_text)
    }

def extract_action_items_nlp(meeting_text: str):
    doc = nlp(meeting_text)
    action_items = []
    for sent in doc.sents:
        # Simple rule: look for sentences with a person and a verb (task)
        persons = [ent.text for ent in sent.ents if ent.label_ == "PERSON"]
        if persons:
            verbs = [token.lemma_ for token in sent if token.pos_ == "VERB"]
            if verbs:
                action_items.append({
                    "owner": persons[0],
                    "task": " ".join([token.text for token in sent if token.pos_ in ["VERB", "NOUN"]]),
                    "deadline": None  # You can add more NLP to extract dates
                })
    return {"provider": "NLP", "action_items": action_items}

def extract_and_schedule_tasks(meeting_text: str, meeting_id: str = None, schedule=True):
    result = run_action_item_tracker(meeting_text)

    from .previous_minutes_service import read_previous_minutes
    meeting_date = None
    next_meeting_date = None
    prev_minutes = read_previous_minutes()
    if prev_minutes:
        meeting_date = prev_minutes.get("date") or prev_minutes.get("meeting_date")
        next_meeting_date = prev_minutes.get("next_meeting_date")

    agenda_items = []
    if meeting_id:
        agenda = read_agenda(meeting_id)
        if agenda:
            agenda_items = agenda.get("agenda", [])

    # Assign durations to action items (for reference, not for scheduling)
    for idx, item in enumerate(result['action_items']):
        if idx < len(agenda_items):
            time_alloc = agenda_items[idx].get("time_allocated", "60 mins")
            try:
                duration = int(time_alloc.split()[0])
            except Exception:
                duration = 60
        else:
            duration = 60
        item["duration"] = duration
        if not item.get("deadline"):
            if next_meeting_date:
                item["deadline"] = next_meeting_date
            elif meeting_date:
                item["deadline"] = meeting_date

    if schedule:
        # 1️⃣ Schedule agenda topics sequentially on next_meeting_date
        if next_meeting_date:
            base_dt = dateparser.parse(next_meeting_date)
            if not base_dt:
                base_dt = datetime.now()
            current_start = base_dt.replace(hour=9, minute=0, second=0, microsecond=0)
            for idx, agenda_item in enumerate(agenda_items):
                topic = agenda_item.get("topic", f"Agenda Item {idx+1}")
                time_alloc = agenda_item.get("time_allocated", "60 mins")
                try:
                    duration = int(time_alloc.split()[0])
                except Exception:
                    duration = 60
                schedule_action_item(
                    task_name=topic,
                    description=f"Agenda topic: {topic}",
                    deadline_str=current_start.strftime("%Y-%m-%d %H:%M"),
                    owner="All",
                    duration_minutes=duration
                )
                current_start += timedelta(minutes=duration)
        # 2️⃣ Schedule each action item as a separate event on its deadline, staggered if same day
        from collections import defaultdict
        deadline_groups = defaultdict(list)
        for item in result['action_items']:
            deadline_groups[item['deadline']].append(item)
        for deadline, items in deadline_groups.items():
            base_dt = dateparser.parse(deadline)
            if not base_dt:
                base_dt = datetime.now()
            current_start = base_dt.replace(hour=9, minute=0, second=0, microsecond=0)
            for item in items:
                task = item.get('task')
                owner = item.get('owner')
                description = f"Action item assigned to {owner}"
                item_duration = item.get("duration", 60)
                schedule_action_item(
                    task_name=task,
                    description=description,
                    deadline_str=current_start.strftime("%Y-%m-%d %H:%M"),
                    owner=owner,
                    duration_minutes=item_duration
                )
                current_start += timedelta(minutes=item_duration)
    if meeting_id:
        save_action_items(meeting_id, result['action_items'])
    return result

def schedule_agenda_and_action_items_from_json():
    # 1. Load previous meeting details
    from .previous_minutes_service import read_previous_minutes
    prev = read_previous_minutes()
    if not prev:
        return {"error": "No previous meeting details found."}
    meeting_id = prev.get("meeting_id")
    next_meeting_date = prev.get("next_meeting_date")
    action_items = prev.get("action_items", [])

    # 2. Load agenda for this meeting
    from .agenda_service import read_agenda
    agenda = read_agenda(meeting_id)
    if not agenda:
        return {"error": f"No agenda found for meeting_id: {meeting_id}"}
    agenda_items = agenda.get("agenda", [])

    # 3. Schedule agenda topics sequentially on next_meeting_date
    import dateparser
    from datetime import datetime, timedelta
    from .calendar_service import schedule_action_item

    base_dt = dateparser.parse(next_meeting_date)
    if not base_dt:
        base_dt = datetime.now()
    current_start = base_dt.replace(hour=9, minute=0, second=0, microsecond=0)
    for idx, agenda_item in enumerate(agenda_items):
        topic = agenda_item.get("topic", f"Agenda Item {idx+1}")
        time_alloc = agenda_item.get("time_allocated", "60 mins")
        try:
            duration = int(time_alloc.split()[0])
        except Exception:
            duration = 60
        # Schedule each topic at the current_start time
        schedule_action_item(
            task_name=topic,
            description=f"Agenda topic: {topic}",
            deadline_str=current_start.strftime("%Y-%m-%d %H:%M"),
            owner="All",
            duration_minutes=duration
        )
        # Increment start time for next topic
        current_start += timedelta(minutes=duration)

    # 4. Schedule each action item on its deadline
    from collections import defaultdict
    deadline_groups = defaultdict(list)
    for item in action_items:
        deadline_groups[item['deadline']].append(item)
    for deadline, items in deadline_groups.items():
        base_dt = dateparser.parse(deadline)
        if not base_dt:
            base_dt = datetime.now()
        current_start = base_dt.replace(hour=9, minute=0, second=0, microsecond=0)
        for item in items:
            task = item.get('task')
            owner = item.get('owner')
            description = f"Action item assigned to {owner}"
            duration = 60  # You can customize per action item if needed
            schedule_action_item(
                task_name=task,
                description=description,
                deadline_str=current_start.strftime("%Y-%m-%d %H:%M"),
                owner=owner,
                duration_minutes=duration
            )
            current_start += timedelta(minutes=duration)

    return {"scheduled_agenda": agenda_items, "scheduled_action_items": action_items}

# ✅ Only run this when executing the script directly
if __name__ == "__main__":
    sample_notes = """
    John will prepare the budget report by Friday.
    Sarah will update the project plan.
    The team should review the design next week.
    """
    action_items = extract_and_schedule_tasks(sample_notes)
    print(action_items)
