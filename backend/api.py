from fastapi import FastAPI, Body, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from agents.agenda_planner.agenda_planner import generate_agenda
from agents.minutes_generator.minutes_generator import generate_minutes
from agents.action_item_tracker.tracker import extract_and_schedule_tasks
from agents.transcription_agent.transcription_agent import transcribe_video
from lib.auth import get_current_user
# MODIFIED: Import new DB functions
from lib.database import get_all_agendas_for_user, get_all_action_items_for_user, get_agenda, get_all_minutes_for_user, get_minutes_by_id
from agents.action_item_tracker.calendar_service import schedule_action_item
import dateparser

app = FastAPI()

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to your frontend's domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ROUTES ---

@app.get("/")
def read_root():
    return {"message": "Welcome to the MinuteMe Backend"}

@app.post("/agenda")
async def create_agenda_endpoint(
    user_input: dict = Body(...),
    current_user: dict = Depends(get_current_user)
):
    """
    Creates a new agenda for the authenticated user.
    """
    try:
        user_id = current_user.get("sub")
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID not found in token.")
        
        print(f"Authenticated request. Generating agenda for user: {user_id}")
        agenda = generate_agenda(user_input, user_id=user_id)
        return agenda
    except Exception as e:
        print(f"Error creating agenda: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/agendas")
async def get_agendas_endpoint(current_user: dict = Depends(get_current_user)):
    """
    Retrieves all agendas for the authenticated user.
    """
    try:
        user_id = current_user.get("sub")
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID not found in token.")
        
        agendas = get_all_agendas_for_user(user_id)
        return agendas
    except Exception as e:
        print(f"Error getting agendas: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/action-items")
async def get_action_items_endpoint(current_user: dict = Depends(get_current_user)):
    """
    Retrieves all action items for the authenticated user.
    """
    try:
        user_id = current_user.get("sub")
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID not found in token.")
        
        action_items = get_all_action_items_for_user(user_id)
        return action_items
    except Exception as e:
        print(f"Error getting action items: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/minutes")
async def get_all_minutes_endpoint(current_user: dict = Depends(get_current_user)):
    """
    Retrieves all minutes documents for the authenticated user.
    """
    user_id = current_user.get("sub")
    minutes = get_all_minutes_for_user(user_id)
    return minutes

@app.get("/minutes/{minutes_id}")
async def get_minute_detail_endpoint(minutes_id: str, current_user: dict = Depends(get_current_user)):
    """
    Retrieves a single minutes document by its ID.
    """
    user_id = current_user.get("sub")
    minute = get_minutes_by_id(minutes_id, user_id)
    if not minute:
        raise HTTPException(status_code=404, detail="Minutes not found.")
    return minute

@app.get("/events")
async def get_events_endpoint(current_user: dict = Depends(get_current_user)):
    """
    Retrieves all agendas and action items formatted as calendar events.
    """
    user_id = current_user.get("sub")
    agendas = get_all_agendas_for_user(user_id)
    action_items = get_all_action_items_for_user(user_id)
    
    events = []
    
    # Process agendas into events
    for agenda in agendas:
        event_date = dateparser.parse(agenda.get("meeting_date"))
        if event_date:
            events.append({
                "title": agenda.get("meeting_name", "Untitled Meeting"),
                "start": event_date,
                "end": event_date,
                "allDay": True,
                "resource": {"type": "agenda"}
            })
            
    # Process action items into events
    for item in action_items:
        deadline = item.get("deadline")
        if deadline:
            deadline_date = dateparser.parse(deadline)
            if deadline_date:
                 events.append({
                    "title": item.get("task", "Untitled Task"),
                    "start": deadline_date,
                    "end": deadline_date,
                    "allDay": True,
                    "resource": {"type": "action_item", "owner": item.get("owner")}
                })

    return events

@app.post("/schedule-agenda")
async def schedule_agenda_endpoint(
    request_body: dict = Body(...),
    current_user: dict = Depends(get_current_user)
):
    """
    Schedules a meeting in Google Calendar based on an agenda_id.
    """
    user_id = current_user.get("sub")
    agenda_id = request_body.get("agenda_id")
    if not agenda_id:
        raise HTTPException(status_code=400, detail="agenda_id is required.")

    agenda = get_agenda(agenda_id, user_id)
    if not agenda:
        raise HTTPException(status_code=404, detail="Agenda not found.")

    try:
        description = "\n".join([item['topic'] for item in agenda.get("agenda", [])])
        schedule_action_item(
            task_name=agenda.get("meeting_name"),
            description=description,
            deadline_str=agenda.get("meeting_date"),
            owner="All",
            duration_minutes=60 # Default duration
        )
        return {"message": "Meeting scheduled successfully in Google Calendar."}
    except Exception as e:
        print(f"Error scheduling agenda: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to schedule meeting: {e}")


@app.post("/transcribe")
async def transcribe_endpoint(
    request_body: dict = Body(...),
    current_user: dict = Depends(get_current_user)
):
    """
    Transcribes a video from a URL for the authenticated user.
    Expects: {"video_url": "http://..."}
    """
    try:
        user_id = current_user.get("sub")
        video_url = request_body.get("video_url")
        if not user_id or not video_url:
            raise HTTPException(status_code=400, detail="User ID or video_url missing.")

        print(f"Authenticated request. Transcribing video for user: {user_id}")
        # Note: The transcription agent saves the transcript to the DB itself.
        # We need to pass the user_id to it.
        transcript_text = transcribe_video(video_url=video_url, user_id=user_id)
        if transcript_text:
            return {"message": "Transcription successful and saved.", "transcript": transcript_text}
        else:
            raise HTTPException(status_code=500, detail="Transcription failed.")
    except Exception as e:
        print(f"Error during transcription: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate-minutes")
async def generate_minutes_endpoint(current_user: dict = Depends(get_current_user)):
    """
    Generates minutes from the latest transcript for the authenticated user.
    """
    try:
        user_id = current_user.get("sub")
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID not found in token.")

        print(f"Authenticated request. Generating minutes for user: {user_id}")
        minutes_data = generate_minutes(user_id=user_id)
        if not minutes_data:
            raise HTTPException(status_code=404, detail="Failed to generate minutes. No transcript found?")
        
        # --- FIX: Convert ObjectId fields to strings ---
        if "_id" in minutes_data and not isinstance(minutes_data["_id"], str):
            minutes_data["_id"] = str(minutes_data["_id"])
        if "meeting_id" in minutes_data and not isinstance(minutes_data["meeting_id"], str):
            minutes_data["meeting_id"] = str(minutes_data["meeting_id"])
        
        return {"message": "Minutes generated successfully.", "minutes": minutes_data}
    except Exception as e:
        print(f"Error generating minutes: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate-action-items")
async def generate_action_items_endpoint(
    request_body: dict = Body(...),
    current_user: dict = Depends(get_current_user)
):
    """
    Generates action items for a specific minutes document.
    Expects: {"minutes_id": "..."}
    """
    try:
        user_id = current_user.get("sub")
        minutes_id = request_body.get("minutes_id")
        if not user_id or not minutes_id:
            raise HTTPException(status_code=400, detail="User ID or minutes_id missing.")

        print(f"Authenticated request. Generating action items for minutes_id: {minutes_id}")
        action_items_result = extract_and_schedule_tasks(user_id=user_id, minutes_id=minutes_id)
        if action_items_result is None:
            raise HTTPException(status_code=404, detail="Minutes document not found.")

        return {
            "message": "Action items generated and scheduled successfully.",
            "action_items_result": action_items_result
        }
    except Exception as e:
        print(f"Error processing action items: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# The old /process-meeting endpoint is now removed.
