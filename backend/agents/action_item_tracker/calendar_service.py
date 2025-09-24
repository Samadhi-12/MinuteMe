import os
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import dateparser

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('calendar', 'v3', credentials=creds)
    return service

def schedule_action_item(task_name: str, description: str, deadline_str: str, owner: str):
    service = get_calendar_service()

    # Convert natural language deadline to datetime
    if deadline_str:
        deadline = dateparser.parse(deadline_str, settings={'PREFER_DATES_FROM': 'future'})
    else:
        deadline = datetime.now() + timedelta(days=2)  # default 2 days later
    start_time = deadline.replace(hour=9, minute=0, second=0, microsecond=0)
    end_time = start_time + timedelta(hours=1)

    event = {
        'summary': f"{task_name} ({owner})",
        'description': description,
        'start': {'dateTime': start_time.isoformat(), 'timeZone': 'Asia/Colombo'},
        'end': {'dateTime': end_time.isoformat(), 'timeZone': 'Asia/Colombo'},
    }

    created_event = service.events().insert(calendarId='primary', body=event).execute()
    print(f"Event created: {created_event.get('htmlLink')}")
    return created_event
