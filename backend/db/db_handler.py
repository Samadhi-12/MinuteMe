from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
import os

# ------------------------
# MongoDB Atlas configuration
# ------------------------
# You can set these as environment variables for security
MONGODB_URI = os.getenv(
    "MONGODB_URI",
    "mongodb+srv://dilaraamashi_db_user:Dilara.mongo12@cluster0.dau7h11.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)
MONGODB_DB = os.getenv("MONGODB_DB", "meeting_assistant")

# Connect to MongoDB Atlas
client = MongoClient(MONGODB_URI)
db = client[MONGODB_DB]

# Collections
transcripts_collection = db["transcripts"]
minutes_collection = db["minutes"]

# ------------------------
# CRUD Functions
# ------------------------
def save_transcript_to_db(meeting_name, video_url, transcript_text, audio_file_path=None):
    """
    Save transcript metadata and text to MongoDB
    """
    doc = {
        "meeting_name": meeting_name,
        "video_url": video_url,
        "transcript_text": transcript_text,
        "audio_file_path": audio_file_path,
        "created_at": datetime.utcnow(),
        "processed_by": "transcription_agent_v1"
    }
    result = transcripts_collection.insert_one(doc)
    return str(result.inserted_id)

def get_transcript_by_id(transcript_id):
    """Fetch a transcript document by its ObjectId string."""
    try:
        doc = transcripts_collection.find_one({"_id": ObjectId(transcript_id)})
        if not doc:
            return None
        doc["_id"] = str(doc["_id"])  # stringify for JSON safety
        return doc
    except Exception:
        return None

def save_minutes_to_db(transcript_id, minutes_doc):
    """Save generated minutes and link to transcript id."""
    doc = {
        "transcript_id": transcript_id,
        "minutes": minutes_doc,
        "created_at": datetime.utcnow(),
        "source": "minutes_generator_v1"
    }
    result = minutes_collection.insert_one(doc)
    return str(result.inserted_id)

def get_minutes_by_id(minutes_id):
    try:
        doc = minutes_collection.find_one({"_id": ObjectId(minutes_id)})
        if not doc:
            return None
        doc["_id"] = str(doc["_id"])  # stringify for JSON safety
        return doc
    except Exception:
        return None
