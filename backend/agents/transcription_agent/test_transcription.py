import gdown
from pathlib import Path
from backend.agents.transcription_agent.transcriber import generate_transcript

# Temporary directory for downloaded video
TEMP_VIDEO_DIR = Path(__file__).parent.parent / "temp_video"
TEMP_VIDEO_DIR.mkdir(exist_ok=True)

# Google Drive file ID for test video
file_id = "1XNPouVTuk-BCX9Y0C7qGSf3Em8PHHpIN"
url = f"https://drive.google.com/uc?id={file_id}"

# Local path to save the video
output_path = TEMP_VIDEO_DIR / "temp_meeting_video.mp4"

# Download the file if not already exists
if not output_path.exists():
    print("[INFO] Downloading video...")
    gdown.download(url, str(output_path), quiet=False)
else:
    print("[INFO] Video already downloaded.")

print("[INFO] Running transcript generation...")
transcript_text = generate_transcript(str(output_path))

# Show results
print("\n[TRANSCRIPT OUTPUT] ------------------")
print(transcript_text)

# Optionally, remove the downloaded video after transcription
if output_path.exists():
    output_path.unlink()
    print("\n[INFO] Temporary video removed.")
