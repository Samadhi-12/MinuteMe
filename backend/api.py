from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from agents.agenda_planner.agenda_planner import generate_agenda
#from agents.minutes_generator.generator import generate_minutes
from agents.action_item_tracker.tracker import extract_and_schedule_tasks

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
    return {
        "agenda": [
            {"topic": "Budget Review", "priority": "urgent", "time_allocated": "20 mins"},
            {"topic": "Project Plan", "priority": "discussion", "time_allocated": "15 mins"},
            {"topic": "Design Review", "priority": "info", "time_allocated": "10 mins"}
        ]
    }

@app.post("/agenda")
def create_agenda(meeting_info: dict = Body(...)):
    return generate_agenda(meeting_info)

#@app.post("/minutes")
#def create_minutes(transcript: dict = Body(...)):
#    return generate_minutes(transcript["text"])

@app.post("/action-items")
def create_action_items(minutes: dict = Body(...)):
    return extract_and_schedule_tasks(minutes)
