import os
import re
import json
from pathlib import Path
from collections import Counter
from rake_nltk import Rake
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


def get_next_meeting_id(output_dir="data/agendas"):
    """Generate next meeting ID based on existing files"""
    files = os.listdir(output_dir) if os.path.exists(output_dir) else []
    meeting_ids = []
    for f in files:
        match = re.match(r"meetingId_(\d+)\.json", f)
        if match:
            meeting_ids.append(int(match.group(1)))
    next_id = max(meeting_ids) + 1 if meeting_ids else 1
    return f"meetingId_{next_id:02d}"


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

def get_user_input_if_no_previous_file():
    """
    Returns user input if previous_meeting/meeting_details.json doesn't exist.
    """
    file_path = "data/previous_meeting/meeting_details.json"
    
    previous_data = load_json(file_path)
    if previous_data:
        # Use future_discussion & next_meeting_date from file
        user_input = {
            "topics": previous_data.get("future_discussion", []),
            "discussion_points": previous_data.get("current_discussion", []),
            "date": previous_data.get("next_meeting_date")
        }
    else:
        # Fallback example (can be replaced by UI input later)
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
            "date": "2025-09-10"
        }
    return user_input
