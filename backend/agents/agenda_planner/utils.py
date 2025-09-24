import os
import re
import json
from pathlib import Path
from collections import Counter

# Optional RAKE import with graceful fallback to a simple extractor
try:
    from rake_nltk import Rake  # type: ignore
except Exception:  # pragma: no cover - environment without rake_nltk
    Rake = None  # fallback handled below
def get_project_root() -> Path:
    """Return the project root directory (repo root).

    This file lives at backend/agents/agenda_planner/utils.py. The repo root
    is one level above the backend directory.
    """
    here = Path(__file__).resolve()
    # utils.py -> agenda_planner -> agents -> backend -> root
    return here.parents[3]


def resolve_data_path(relative_path: str) -> Path:
    """Resolve a data path relative to the project root.

    Also supports legacy paths under `backend/data/...` if top-level `data/...`
    does not exist.
    """
    # Normalize common '../data/...' to top-level 'data/...'
    if relative_path.startswith("../data/"):
        relative_path = relative_path[3:]

    root = get_project_root()
    rel = Path(relative_path)
    primary = (root / rel).resolve()
    if primary.exists() or primary.parent.exists():
        return primary
    # Fallback to backend/data for historical layouts
    if relative_path.startswith("data/"):
        fallback = (root / ("backend/" + relative_path)).resolve()
        return fallback
    return primary


def load_json(file_path):
    """Load JSON data from a file. Accepts absolute or repo-relative paths."""
    path = Path(file_path)
    if not path.is_absolute():
        path = resolve_data_path(file_path)
    if not path.exists():
        return None
    with open(path, "r") as f:
        return json.load(f)


def save_json(data, file_path):
    """Save JSON data to a file at a repo-relative path by default."""
    path = Path(file_path)
    if not path.is_absolute():
        path = resolve_data_path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


def save_text(text: str, file_path: str) -> None:
    """Save plain text content to a file, resolving repo-relative paths."""
    path = Path(file_path)
    if not path.is_absolute():
        path = resolve_data_path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def get_next_meeting_id(output_dir="backend/data/agendas"):
    """Generate next meeting ID based on existing agendas.

    Supports either legacy flat files named meetingId_XX.json in output_dir
    or the new layout with subfolders named meetingId_XX/.
    """
    output_path = resolve_data_path(output_dir)
    entries = os.listdir(output_path) if os.path.exists(output_path) else []
    meeting_ids = []
    for name in entries:
        # Subfolder layout: meetingId_XX/
        dir_match = re.match(r"meetingId_(\d+)$", name)
        if dir_match and os.path.isdir(os.path.join(output_path, name)):
            meeting_ids.append(int(dir_match.group(1)))
            continue
        # Legacy flat-file layout: meetingId_XX.json
        file_match = re.match(r"meetingId_(\d+)\.json$", name)
        if file_match:
            meeting_ids.append(int(file_match.group(1)))
    next_id = max(meeting_ids) + 1 if meeting_ids else 1
    return f"meetingId_{next_id:02d}"


def extract_keywords_tfidf(texts, top_n=5):
    """Basic TF-IDF-like keyword extraction without external dependencies.

    This is a lightweight fallback to avoid requiring scikit-learn.
    """
    if isinstance(texts, str):
        texts = [texts]
    # Very small stopword list to avoid overfitting
    stopwords = {
        "the", "and", "or", "of", "to", "in", "for", "on", "a", "an",
        "is", "are", "was", "were", "with", "by", "at", "from", "as",
    }
    # Term frequencies per document
    doc_tokens = []
    df_counter = Counter()
    for t in texts:
        tokens = [w.lower() for w in re.findall(r"[a-zA-Z][a-zA-Z\-]+", t)]
        tokens = [w for w in tokens if w not in stopwords]
        unique_tokens = set(tokens)
        for tok in unique_tokens:
            df_counter[tok] += 1
        tf_counter = Counter(tokens)
        doc_tokens.append(tf_counter)
    num_docs = max(1, len(texts))
    # Score = sum over docs of tf * idf, where idf = log(N / (1+df))
    import math
    scores = Counter()
    for tf_counter in doc_tokens:
        for tok, tf in tf_counter.items():
            idf = math.log(num_docs / (1 + df_counter[tok]))
            scores[tok] += tf * idf
    return [w for w, _ in scores.most_common(top_n)]


def extract_keywords_rake(text, top_n=5):
    """Extract keywords using RAKE (if available) or fallback to TF-IDF.

    Returns only phrases/words without scores.
    """
    if isinstance(text, list):
        text = " ".join(text)
    if Rake is not None:
        try:
            rake = Rake()
            rake.extract_keywords_from_text(text)
            phrases_with_scores = rake.get_ranked_phrases_with_scores()
            return [phrase for score, phrase in phrases_with_scores[:top_n]]
        except Exception:
            pass
    # Fallback: simple TF-IDF keywords
    return extract_keywords_tfidf([text], top_n=top_n)

def _prompt_user_for_next_meeting() -> dict:
    """Prompt user in the console for next meeting details.

    Returns a dict with keys: topics, discussion_points, date
    """
    print("No previous meeting record found. Please provide brief details for the next meeting.")
    try:
        raw_topics = input("Enter main topics (comma-separated): ").strip()
        raw_discussion = input("Enter discussion points (comma-separated): ").strip()
        date_str = input("Enter meeting date (YYYY-MM-DD), or leave blank for today: ").strip()
    except (EOFError, KeyboardInterrupt):
        # Fall back to defaults when running non-interactively
        return {
            "topics": [
                "Team updates",
                "Upcoming priorities"
            ],
            "discussion_points": [
                "Review action items",
                "Plan next sprint"
            ],
            "date": None
        }

    topics = [t.strip() for t in raw_topics.split(",") if t.strip()] if raw_topics else []
    discussion_points = [d.strip() for d in raw_discussion.split(",") if d.strip()] if raw_discussion else []
    date_val = date_str or None
    return {
        "topics": topics,
        "discussion_points": discussion_points,
        "date": date_val,
    }


def get_user_input_if_no_previous_file():
    """
    Returns user input if previous_meeting/meeting_details.json doesn't exist.
    """
    file_path = "data/previous_meetings/meeting_details.json"
    
    previous_data = load_json(file_path)
    if previous_data:
        # Use future_discussion & next_meeting_date from file
        user_input = {
            "topics": previous_data.get("future_discussion", []),
            "discussion_points": previous_data.get("current_discussion", []),
            "date": previous_data.get("next_meeting_date")
        }
    else:
        # Prompt the user interactively; fallback defaults if not possible
        user_input = _prompt_user_for_next_meeting()
    return user_input
