import os
import json
import spacy
from transformers import pipeline

# Define file paths as constants
TRANSCRIPT_INPUT_PATH = os.path.join('data', 'transcript_meeting', 'transcript_meeting.json')
MINUTES_OUTPUT_PATH = os.path.join('data', 'previous_meeting', 'meeting_details.json')

def load_transcript(file_path: str) -> str:
    """Loads the transcript text from a JSON file."""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            return data.get("transcript", "")
    except FileNotFoundError:
        print(f"Error: Transcript file not found at {file_path}")
        return ""
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {file_path}")
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
    """Extracts key decisions from the text using NLP rules."""
    print("Extracting key decisions...")
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    decisions = []
    # Keywords that often indicate a decision has been made
    decision_keywords = ["we will", "we decided", "the decision is", "agreed to", "will proceed with"]
    for sent in doc.sents:
        if any(keyword in sent.text.lower() for keyword in decision_keywords):
            decisions.append(sent.text.strip())
    print(f"Found {len(decisions)} potential decisions.")
    return decisions

def extract_future_topics(text: str) -> list:
    """Extracts potential future topics from the text using NLP rules."""
    print("Extracting future topics...")
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    future_topics = []
    # Keywords that often indicate a future topic
    future_keywords = ["next meeting", "discuss later", "in the future", "next time we should"]
    for sent in doc.sents:
        if any(keyword in sent.text.lower() for keyword in future_keywords):
            future_topics.append(sent.text.strip())
    print(f"Found {len(future_topics)} potential future topics.")
    return future_topics

def generate_minutes(transcript_path: str, output_path: str):
    """Main function to generate and save meeting minutes."""
    print("\n--- 🚀 Starting Minutes Generator ---")
    transcript = load_transcript(transcript_path)
    if not transcript:
        print("Aborting: No transcript content to process.")
        return

    summary = generate_summary(transcript)
    decisions = extract_key_decisions(transcript)
    future_topics = extract_future_topics(transcript)

    # Structure the output to be compatible with the action_item_tracker
    output_data = {
        "meeting_id": "generated_from_transcript", # This could be dynamic in a real app
        "date": "2025-10-13", # Placeholder date
        "next_meeting_date": "2025-10-20", # Placeholder date
        "summary": summary,
        "decisions": decisions,
        "future_discussion_points": future_topics, # Added future topics
        "action_items": [] # The action_item_tracker will populate this later
    }
    print(f"📝 Prepared minutes data with {len(decisions)} decisions and {len(future_topics)} future topics.")

    # Ensure the output directory exists
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    # Save the structured minutes
    with open(output_path, 'w') as f:
        json.dump(output_data, f, indent=2)

    print(f"✅ Meeting minutes successfully generated and saved to {output_path}")
    print("--- ✨ Finished Minutes Generator ---\n")
    return output_data

if __name__ == '__main__':
    # This allows you to run the script directly to generate minutes
    # from the existing transcript file.
    # Run from the `backend` directory:
    # python -m agents.minutes_generator.minutes_generator
    generate_minutes(TRANSCRIPT_INPUT_PATH, MINUTES_OUTPUT_PATH)