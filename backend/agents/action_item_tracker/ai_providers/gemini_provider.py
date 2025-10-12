import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
import re

load_dotenv()
genai.configure(api_key = os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def clean_json_output(raw_output: str):
    try:
        return json.loads(raw_output)
    except:
        match = re.search(r"\[.*]", raw_output, re.DOTALL)
        if match:
            return json.loads(match.group())
        return [{"error": "Failed to parse", "raw": raw_output}]
    
def extract_action_items(meeting_text:str):
    prompt = f"""
    Extract action items from this meeting. Respond ONLY with JSON list of objects.
    Each object must have: owner, task, deadline (if any).
    Meeting text: {meeting_text}
    """
    response = model.generate_content(prompt)
    return clean_json_output(response.text)


###########################################################
#Sample Output
#[
#  {"owner": "John", "task": "Prepare budget", "deadline": "Friday"},
#  {"owner": "Sarah", "task": "Update project plan", "deadline": null}
#]