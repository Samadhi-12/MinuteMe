from fastapi import FastAPI, Body, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from agents.agenda_planner.agenda_planner import generate_agenda
from agents.minutes_generator.minutes_generator import generate_minutes
from agents.action_item_tracker.tracker import extract_and_schedule_tasks
from agents.transcription_agent.transcription_agent import transcribe_video
from lib.auth import get_current_user
# MODIFIED: Import new DB functions
from lib.database import (
    get_db,  # <-- Add this
    get_all_agendas_for_user,
    get_all_action_items_for_user,
    get_agenda,
    get_all_minutes_for_user,
    get_minutes_by_id,
    update_agenda,
    save_meeting,
    get_all_meetings_for_user,
    update_meeting,
    delete_meeting
)
from agents.action_item_tracker.calendar_service import schedule_action_item
import dateparser
from bson import ObjectId
from datetime import datetime

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
    user_id = current_user.get("sub")
    meetings = get_all_meetings_for_user(user_id)
    action_items = get_all_action_items_for_user(user_id)  # <-- Add this

    events = []

    # Meetings as events
    for meeting in meetings:
        event_date = dateparser.parse(meeting.get("meeting_date"))
        if event_date:
            events.append({
                "title": meeting.get("meeting_name", "Untitled Meeting"),
                "start": event_date,
                "end": event_date,
                "allDay": True,
                "resource": {
                    "type": "meeting",
                    "agenda_id": meeting.get("agenda_id")
                }
            })

    # Action items as events
    for item in action_items:
        deadline = item.get("deadline")
        if deadline:
            deadline_date = dateparser.parse(deadline)
            if deadline_date:
                events.append({
                    "title": f"Action: {item.get('task', 'Task')}",
                    "start": deadline_date,
                    "end": deadline_date,
                    "allDay": True,
                    "resource": {
                        "type": "action-item",
                        "owner": item.get("owner"),
                        "status": item.get("status"),
                        "minutes_id": item.get("minutes_id")
                    }
                })

    return events

@app.post("/schedule-agenda")
async def schedule_agenda_endpoint(
    request_body: dict = Body(...),
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user.get("sub")
    agenda_id = request_body.get("agenda_id")
    if not agenda_id:
        raise HTTPException(status_code=400, detail="agenda_id is required.")

    agenda = get_agenda(agenda_id, user_id)
    if not agenda:
        raise HTTPException(status_code=404, detail="Agenda not found.")

    try:
        description = "\n".join([item['topic'] for item in agenda.get("agenda", [])])
        # Schedule in Google Calendar
        schedule_action_item(
            task_name=agenda.get("meeting_name"),
            description=description,
            deadline_str=agenda.get("meeting_date"),
            owner="All",
            duration_minutes=60
        )
        # Create meeting document in DB
        meeting_data = {
            "meeting_name": agenda.get("meeting_name"),
            "meeting_date": agenda.get("meeting_date"),
            "agenda_id": agenda.get("meeting_id"),
            "status": "scheduled"
        }
        from lib.database import save_meeting
        save_meeting(meeting_data, user_id)
        return {"message": "Meeting scheduled successfully in Google Calendar and saved in DB."}
    except Exception as e:
        print(f"Error scheduling agenda: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to schedule meeting: {e}")


@app.post("/transcribe")
async def transcribe_endpoint(
    request_body: dict = Body(...),
    current_user: dict = Depends(get_current_user)
):
    try:
        user_id = current_user.get("sub")
        video_url = request_body.get("video_url")
        meeting_date = request_body.get("meeting_date")
        meeting_name = request_body.get("meeting_name")
        meeting_id = request_body.get("meeting_id")
        
        print(f"[DEBUG] Transcribe request: user_id={user_id}, meeting_id={meeting_id}, video_url={video_url}")

        if not user_id or not video_url:
            raise HTTPException(status_code=400, detail="User ID or video_url missing.")

        db = get_db()
        # Prevent duplicate transcript for the same meeting
        if meeting_id:
            existing = db.transcripts.find_one({"meeting_id": meeting_id, "user_id": user_id})
            if existing:
                print(f"[DEBUG] Transcript already exists for meeting {meeting_id}. Aborting new transcription.")
                existing["_id"] = str(existing["_id"])
                return {"message": "Transcript already exists for this meeting.", "transcript": existing}

        print(f"Authenticated request. Transcribing video for user: {user_id}")
        # This function should now ONLY return text
        transcript_text = transcribe_video(video_url=video_url, user_id=user_id)
        
        # This is now the ONLY place the transcript is saved
        transcript_data = {
            "user_id": user_id,
            "transcript": transcript_text,
            "created_at": datetime.utcnow(),
            "meeting_date": meeting_date,
            "meeting_name": meeting_name,
            "meeting_id": meeting_id
        }
        
        print(f"[DEBUG] Saving transcript for meeting {meeting_id}")
        result = db.transcripts.insert_one(transcript_data)
        print(f"[DEBUG] Transcript saved with ID: {result.inserted_id}")

        transcript_data["_id"] = str(result.inserted_id)
        return {"message": "Transcription successful and saved.", "transcript": transcript_data}
    except Exception as e:
        print(f"[DEBUG] Error during transcription: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/transcripts")
async def get_transcripts_endpoint(current_user: dict = Depends(get_current_user)):
    """
    Retrieves all transcripts for the authenticated user.
    """
    user_id = current_user.get("sub")
    db = get_db()
    transcripts = list(db.transcripts.find({"user_id": user_id}))
    for t in transcripts:
        t["_id"] = str(t["_id"])
    return transcripts

@app.post("/generate-minutes")
async def generate_minutes_endpoint(request_body: dict = Body(None), current_user: dict = Depends(get_current_user)):
    """
    Generates minutes from the latest transcript for the authenticated user.
    """
    try:
        user_id = current_user.get("sub")
        transcript_id = request_body.get("transcript_id") if request_body else None
        # If transcript_id is provided, use it; else use latest
        minutes_data = generate_minutes(user_id=user_id, transcript_id=transcript_id)
        if not minutes_data:
            raise HTTPException(status_code=404, detail="Failed to generate minutes. No transcript found?")
        
        # Convert ObjectId fields to strings
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


@app.patch("/agenda/{agenda_id}")
async def update_agenda_endpoint(
    agenda_id: str,
    update_data: dict = Body(...),
    current_user: dict = Depends(get_current_user)
):
    """
    Updates an existing agenda for the authenticated user.
    """
    user_id = current_user.get("sub")
    # Implement update logic in lib/database.py
    updated_agenda = update_agenda(agenda_id, update_data, user_id)
    if not updated_agenda:
        raise HTTPException(status_code=404, detail="Agenda not found or update failed.")
    return updated_agenda

@app.patch("/action-items/{item_id}")
async def update_action_item_status(
    item_id: str,
    update_data: dict = Body(...),
    current_user: dict = Depends(get_current_user)
):
    """
    Updates the status or details of an action item.
    """
    user_id = current_user.get("sub")
    db = get_db()
    result = db.action_items.update_one(
        {"_id": ObjectId(item_id), "user_id": user_id},
        {"$set": update_data}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Action item not found or update failed.")
    item = db.action_items.find_one({"_id": ObjectId(item_id), "user_id": user_id})
    if item and "_id" in item:
        item["_id"] = str(item["_id"])
    return item

@app.post("/meetings")
async def create_meeting_endpoint(
    meeting_data: dict = Body(...),
    current_user: dict = Depends(get_current_user)
):
    """
    Creates a new meeting for the authenticated user.
    """
    user_id = current_user.get("sub")
    meeting = save_meeting(meeting_data, user_id)
    return meeting

@app.get("/meetings")
async def get_meetings_endpoint(current_user: dict = Depends(get_current_user)):
    """
    Retrieves all meetings for the authenticated user.
    """
    user_id = current_user.get("sub")
    meetings = get_all_meetings_for_user(user_id)
    return meetings

@app.patch("/meetings/{meeting_id}")
async def update_meeting_endpoint(
    meeting_id: str,
    update_data: dict = Body(...),
    current_user: dict = Depends(get_current_user)
):
    """
    Updates an existing meeting for the authenticated user.
    """
    user_id = current_user.get("sub")
    updated_meeting = update_meeting(meeting_id, update_data, user_id)
    if not updated_meeting:
        raise HTTPException(status_code=404, detail="Meeting not found or update failed.")
    return updated_meeting

@app.delete("/meetings/{meeting_id}")
async def delete_meeting_endpoint(
    meeting_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Deletes a meeting for the authenticated user.
    """
    user_id = current_user.get("sub")
    deleted = delete_meeting(meeting_id, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Meeting not found or delete failed.")
    return {"message": "Meeting deleted."}
