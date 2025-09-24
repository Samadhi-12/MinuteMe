# backend/agents/test_agents.py

import os
from pathlib import Path
from backend.agents.transcription_agent.transcriber import generate_transcript
from backend.agents.minutes_generator.minutes_generator import generate_minutes
from backend.db.db_handler import save_transcript_to_db, save_minutes_to_db
import gdown  # make sure gdown is installed: pip install gdown

# -----------------------------
# CONFIG
# -----------------------------
DRIVE_URL = "https://drive.google.com/file/d/1C_KOZvxM3Mal0za6jkTAq1l0HbZwC-pe/view?usp=drive_link"
VIDEO_NAME = "Test_Meeting_001_drive.mp4"
MEETING_NAME = "Test Meeting 001"
VIDEO_PATH = Path("temp_uploads") / VIDEO_NAME

# Ensure temp directory exists
VIDEO_PATH.parent.mkdir(exist_ok=True)

# -----------------------------
# Download video from Google Drive
# -----------------------------
if not VIDEO_PATH.exists():
    print(f"[INFO] Downloading video from Google Drive...")
    # gdown needs "file id" not full URL
    file_id = DRIVE_URL.split("/d/")[1].split("/")[0]
    gdown.download(f"https://drive.google.com/uc?id={file_id}", str(VIDEO_PATH), quiet=False)
    print(f"[INFO] Video downloaded successfully to {VIDEO_PATH}")

# -----------------------------
# Generate transcript locally
# -----------------------------
print(f"[INFO] Generating transcript for: {VIDEO_PATH}...")
transcript_text = generate_transcript(str(VIDEO_PATH))
print("[INFO] Transcript generated successfully!")

# -----------------------------
# Generate structured minutes
# -----------------------------
minutes_doc = generate_minutes(transcript_text)
print("[INFO] Minutes generated successfully!")

# -----------------------------
# Save transcript to MongoDB
# -----------------------------
transcript_id = save_transcript_to_db(
    meeting_name=MEETING_NAME,
    video_url=DRIVE_URL,
    transcript_text=transcript_text,
    audio_file_path=str(VIDEO_PATH)
)

# -----------------------------
# Save minutes to MongoDB
# -----------------------------
minutes_id = save_minutes_to_db(transcript_id, minutes_doc)

# -----------------------------
# Display results
# -----------------------------
print("\n[RESULT] --- Transcript & Minutes ---")
print(f"Transcript ID: {transcript_id}")
print(f"Minutes ID: {minutes_id}")
print(f"Meeting Name: {MEETING_NAME}\n")

print("Transcript:\n", transcript_text)
print("\nMinutes:\n", minutes_doc)
