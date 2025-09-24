# backend/agents/transcription_agent/app.py

from flask import Flask, request, jsonify
from pathlib import Path
import uuid
from .transcriber import generate_transcript
from .utils import ensure_dir
from backend.db.db_handler import save_transcript_to_db, save_minutes_to_db
from backend.agents.minutes_generator.minutes_generator import generate_minutes

app = Flask(__name__)

# Directory to temporarily store uploaded/downloaded videos
UPLOAD_DIR = Path("temp_uploads")
ensure_dir(UPLOAD_DIR)

@app.route("/transcribe", methods=["POST"])
def transcribe():
    """
    Accepts either:
    1. A video file upload via 'file'
    2. A video URL via 'video_url'
    Automatically generates and saves minutes after transcription.
    """
    meeting_name = request.form.get("meeting_name", "meeting_" + str(uuid.uuid4()))
    source_video_url = None
    video_path = None

    # ------------------------
    # Handle video file upload
    # ------------------------
    if "file" in request.files:
        file = request.files["file"]
        save_path = UPLOAD_DIR / file.filename
        file.save(save_path)
        video_path = save_path

    # ------------------------
    # Handle video URL
    # ------------------------
    elif "video_url" in request.form:
        import requests
        video_url = request.form["video_url"]
        source_video_url = video_url
        local_filename = UPLOAD_DIR / f"{meeting_name}.mp4"
        r = requests.get(video_url, stream=True)
        with open(local_filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        video_path = local_filename

    else:
        return jsonify({"error": "No video file or URL provided"}), 400

    try:
        # ------------------------
        # Generate transcript using local file
        # ------------------------
        transcript_text = generate_transcript(str(video_path))

        # ------------------------
        # Save transcript to MongoDB
        # ------------------------
        transcript_id = save_transcript_to_db(
            meeting_name=meeting_name,
            video_url=source_video_url,
            transcript_text=transcript_text,
            audio_file_path=str(video_path)
        )

        # ------------------------
        # Generate structured minutes
        # ------------------------
        minutes_doc = generate_minutes(transcript_text)

        # ------------------------
        # Save minutes to MongoDB
        # ------------------------
        minutes_id = save_minutes_to_db(transcript_id, minutes_doc)

    except Exception as e:
        return jsonify({"error": f"Processing failed: {e}"}), 500

    # ------------------------
    # Do NOT delete the local video immediately
    # You can clean temp files manually later if needed
    # ------------------------

    # ------------------------
    # Return results
    # ------------------------
    return jsonify({
        "transcript_id": transcript_id,
        "minutes_id": minutes_id,
        "meeting_name": meeting_name,
        "transcript": transcript_text,
        "minutes": minutes_doc
    })


if __name__ == "__main__":
    print(f"[INFO] Upload directory: {UPLOAD_DIR.resolve()}")
    print("[INFO] Flask server running on http://127.0.0.1:5001")
    app.run(debug=True, port=5001)
