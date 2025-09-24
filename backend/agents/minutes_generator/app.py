# backend/agents/minutes_generator/app.py

from flask import Flask, request, jsonify
from backend.db.db_handler import get_transcript_by_id, save_minutes_to_db
from .minutes_generator import generate_minutes

app = Flask(__name__)

@app.route("/generate_minutes", methods=["POST"])
def generate_minutes_route():
    transcript_id = request.form.get("transcript_id")
    if not transcript_id:
        return jsonify({"error": "transcript_id is required"}), 400

    transcript_doc = get_transcript_by_id(transcript_id)
    if not transcript_doc:
        return jsonify({"error": "Transcript not found"}), 404

    transcript_text = transcript_doc["transcript_text"]
    minutes_doc = generate_minutes(transcript_text)
    minutes_id = save_minutes_to_db(transcript_id, minutes_doc)

    return jsonify({
        "minutes_id": minutes_id,
        "minutes_doc": minutes_doc
    })

if __name__ == "__main__":
    app.run(debug=True, port=5002)
