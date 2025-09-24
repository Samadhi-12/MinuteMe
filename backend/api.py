from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from agents.agenda_planner.agenda_planner import generate_agenda
from agents.minutes_generator.minutes_generator import MinutesGenerator
from agents.action_item_tracker.tracker import extract_and_schedule_tasks
from agents.action_item_tracker.previous_minutes_service import read_previous_minutes

app = FastAPI()

# Allow frontend (localhost:3000 for React dev server) to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


#ROUTES

@app.get("/agenda")
def get_agenda():
    # Returns the latest agenda, or a default if none exist
    return generate_agenda()

@app.post("/agenda")
def create_agenda(meeting_info: dict = Body(...)):
    return generate_agenda(meeting_info)


# Create a singleton MinutesGenerator instance
minutes_generator = MinutesGenerator()

@app.post("/minutes")
def create_minutes(transcript: dict = Body(...)):
    return minutes_generator.generate_minutes(transcript["text"])

@app.get("/action-items")
async def get_action_items():
    # Get action items from the tracker's database/storage
    # Note: You might want to implement a storage solution later
    result = extract_and_schedule_tasks("", schedule=False)
    return result

@app.post("/action-items")
def create_action_items(minutes: dict = Body(...)):
    meeting_id = minutes.get("meeting_id", "default")
    meeting_text = minutes.get("text", "")
    return extract_and_schedule_tasks(meeting_text, meeting_id=meeting_id)

@app.patch("/action-items/{item_id}/status")
async def update_action_item_status(item_id: int, status_update: dict = Body(...)):
    # In a real application, you would update this in a database
    return {"message": f"Updated status for item {item_id}"}

@app.post("/schedule-previous-action-items")
def schedule_previous_action_items():
    from agents.action_item_tracker.tracker import schedule_agenda_and_action_items_from_json
    return schedule_agenda_and_action_items_from_json()
