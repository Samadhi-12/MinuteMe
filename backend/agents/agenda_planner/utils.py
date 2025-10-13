import os
import re
import json
from pathlib import Path
from collections import Counter

# Ensure NLTK stopwords and punkt are downloaded
import nltk
for resource in ['stopwords', 'punkt']:
    try:
        nltk.data.find(f'corpora/{resource}' if resource == 'stopwords' else f'tokenizers/{resource}')
    except LookupError:
        nltk.download(resource)
from rake_nltk import Rake
from lib.database import get_document_count # Import the new DB function
# Import the service that reads from the DB
from ..action_item_tracker.previous_minutes_service import read_previous_minutes

# Ensure NLTK stopwords are downloaded
import nltk
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')
from sklearn.feature_extraction.text import TfidfVectorizer


def load_json(file_path):
    """Load JSON data from a file"""
    if not os.path.exists(file_path):
        return None
    with open(file_path, "r") as f:
        return json.load(f)


def save_json(data, file_path):
    """Save JSON data to a file"""
    Path(os.path.dirname(file_path)).mkdir(parents=True, exist_ok=True)
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)


def get_next_meeting_id(user_id: str):
    """Generate next meeting ID based on count in DB for that user."""
    count = get_document_count("agendas", user_id)
    next_id = count + 1
    return f"meetingId_{user_id}_{next_id:02d}"


def extract_keywords_tfidf(texts, top_n=5):
    """Extract keywords using TF-IDF"""
    vectorizer = TfidfVectorizer(stop_words="english")
    X = vectorizer.fit_transform(texts)
    scores = zip(vectorizer.get_feature_names_out(), X.toarray().sum(axis=0))
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    return [word for word, score in sorted_scores[:top_n]]


def extract_keywords_rake(text, top_n=5):
    """Extract keywords using RAKE and return only phrases (not scores)"""
    rake = Rake()
    if isinstance(text, list):
        text = " ".join(text)  # join list into string
    rake.extract_keywords_from_text(text)
    # get_ranked_phrases_with_scores() returns [(score, phrase), ...]
    phrases_with_scores = rake.get_ranked_phrases_with_scores()
    # Extract only phrases
    keywords = [phrase for score, phrase in phrases_with_scores[:top_n]]
    return keywords

def get_user_input_if_no_previous_file(user_id: str):
    """
    Returns user input based on the last meeting's minutes from the database.
    """
    # This now correctly reads from the database via the service
    previous_data = read_previous_minutes(user_id)
    
    if previous_data:
        print("🧠 Found previous minutes in DB. Generating topics for next meeting.")
        # Use future_discussion & next_meeting_date from the DB document
        user_input = {
            "topics": previous_data.get("future_discussion_points", []),
            "discussion_points": [item.get("task", "") for item in previous_data.get("action_items", [])],
            "date": previous_data.get("next_meeting_date")
        }
    else:
        # Fallback example if no minutes exist for the user in the DB
        print("⚠️ No previous minutes in DB. Using default example topics.")
        user_input = {
            "topics": [
                "Social Media Campaign Review",
                "Q4 Advertising Budget"
            ],
            "discussion_points": [
                "Analyze recent email marketing performance",
                "Plan upcoming influencer collaborations",
                "Evaluate content strategy effectiveness"
            ],
            "date": "2025-10-20"
        }
    return user_input
