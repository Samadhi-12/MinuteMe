import os
import json
import nltk
from transformers import pipeline
from lib.database import save_minutes, get_latest_transcript
from datetime import datetime, timedelta
from bson.objectid import ObjectId

# Ensure NLTK sentence tokenizer is downloaded
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

def load_transcript_from_db(user_id: str, transcript_id: str = None) -> str:
    """Loads a transcript text for a user from MongoDB. If transcript_id is provided, loads that specific transcript."""
    print(f"📖 Loading transcript from DB for user: {user_id}")
    from lib.database import get_latest_transcript, get_db
    db = get_db()
    if transcript_id:
        transcript_doc = db.transcripts.find_one({"_id": ObjectId(transcript_id), "user_id": user_id})
    else:
        transcript_doc = get_latest_transcript(user_id)
    if transcript_doc:
        return transcript_doc.get("transcript", "")
    print("⚠️ No transcript found in DB.")
    return ""

def generate_summary(text: str) -> str:
    """Generates a summary of the text using a local transformer model."""
    print("Generating summary...")
    # Using a pre-trained model for summarization
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    # The model works best on text up to 1024 tokens. We'll truncate if necessary.
    max_chunk_length = 1024
    summary = summarizer(text[:max_chunk_length], max_length=150, min_length=40, do_sample=False)
    print("Summary generated.")
    return summary[0]['summary_text']

def extract_key_decisions(text: str) -> list:
    """Extracts key decisions from the text using NLTK."""
    print("Extracting key decisions...")
    decisions = []
    # Keywords that often indicate a decision has been made
    decision_keywords = ["we will", "we decided", "the decision is", "agreed to", "will proceed with"]
    for sent in nltk.sent_tokenize(text):
        if any(keyword in sent.lower() for keyword in decision_keywords):
            decisions.append(sent.strip())
    print(f"Found {len(decisions)} potential decisions.")
    return decisions

def extract_future_topics(text: str) -> list:
    """Extracts potential future topics from the text using NLTK."""
    print("Extracting future topics...")
    future_topics = []
    # Keywords that often indicate a future topic
    future_keywords = ["next meeting", "discuss later", "in the future", "next time we should"]
    for sent in nltk.sent_tokenize(text):
        if any(keyword in sent.lower() for keyword in future_keywords):
            future_topics.append(sent.strip())
    print(f"Found {len(future_topics)} potential future topics.")
    return future_topics

def generate_minutes(user_id: str = "user_placeholder_123", transcript_id: str = None, transcript_text: str = None):
    """Main function to generate and save meeting minutes to MongoDB."""
    print("\n--- 🚀 Starting Minutes Generator ---")
    
    transcript = ""
    if transcript_text:
        print("🧠 Using provided transcript text.")
        transcript = transcript_text
    elif transcript_id or user_id:
        # This now reads from the database instead of a file
        transcript = load_transcript_from_db(user_id, transcript_id)
    
    if not transcript:
        print("Aborting: No transcript content to process.")
        return

    summary = generate_summary(transcript)
    decisions = extract_key_decisions(transcript)
    future_topics = extract_future_topics(transcript)

    # Structure the output to be saved in the 'minutes' collection
    output_data = {
        "meeting_id": f"minutes_{user_id}_{datetime.now().strftime('%Y%m%d')}",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "next_meeting_date": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
        "summary": summary,
        "decisions": decisions,
        "future_discussion_points": future_topics,
        "action_items": [] # The action_item_tracker will populate this later
    }
    print(f"📝 Prepared minutes data with {len(decisions)} decisions and {len(future_topics)} future topics.")

    # Save the structured minutes to MongoDB
    inserted_id = save_minutes(output_data, user_id)
    output_data['_id'] = inserted_id # Add the ID to the returned data

    print(f"✅ Meeting minutes successfully saved to MongoDB with ID: {inserted_id}")
    print("--- ✨ Finished Minutes Generator ---\n")
    return output_data

if __name__ == '__main__':
    # This allows you to run the script directly to generate minutes
    # from the latest transcript in the DB.
    generate_minutes()