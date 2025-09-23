"""
Meeting Summarizer using LLM and NLP techniques for advanced text processing.
Implements text summarization and key sentence extraction.
"""

import os
import re
from typing import Dict, List, Optional, Any
from openai import OpenAI
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class MeetingSummarizer:
    """
    Summarizes meeting content using LLM and NLP techniques.
    
    Features:
    - LLM-powered summarization
    - Key sentence extraction
    - Decision identification
    - Action item extraction
    """
    
    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        """
        Initialize the summarizer.
        
        Args:
            model_name: LLM model to use ("gpt-3.5-turbo", "gpt-4", "gemini-pro")
        """
        self.model_name = model_name
        self.client = None
        self.gemini_model = None
        
        # Initialize appropriate LLM client
        if model_name.startswith("gpt"):
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                self.client = OpenAI(api_key=api_key)
            else:
                print("⚠️ OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
        
        elif model_name.startswith("gemini"):
            api_key = os.getenv("GOOGLE_API_KEY")
            if api_key:
                genai.configure(api_key=api_key)
                self.gemini_model = genai.GenerativeModel('gemini-pro')
            else:
                print("⚠️ Google API key not found. Set GOOGLE_API_KEY environment variable.")
    
    def summarize_meeting(
        self, 
        transcript_text: str, 
        processed_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Summarize meeting content and extract key insights.
        
        Args:
            transcript_text: Raw transcript text
            processed_data: Data processed by TranscriptProcessor
            
        Returns:
            Dictionary containing summarized information
        """
        if not self.client and not self.gemini_model:
            print("⚠️ No LLM client available. Using rule-based summarization.")
            return self._rule_based_summarization(transcript_text, processed_data)
        
        # Use LLM for advanced summarization
        summary_data = {
            "meeting_summary": self._generate_meeting_summary(transcript_text),
            "key_decisions": self._extract_key_decisions(transcript_text),
            "action_items": self._extract_action_items(transcript_text),
            "discussion_highlights": self._extract_discussion_highlights(transcript_text),
            "agenda_summary": self._summarize_agenda_items(processed_data.get("agenda_items", [])),
            "next_steps": self._extract_next_steps(transcript_text)
        }
        
        return summary_data
    
    def _generate_meeting_summary(self, transcript_text: str) -> str:
        """Generate a concise meeting summary."""
        prompt = f"""
        Please provide a concise summary of this meeting transcript. Focus on:
        1. Main topics discussed
        2. Key outcomes
        3. Important decisions made
        4. Next steps identified
        
        Transcript:
        {transcript_text[:2000]}  # Limit to avoid token limits
        
        Summary (2-3 paragraphs):
        """
        
        return self._call_llm(prompt)
    
    def _extract_key_decisions(self, transcript_text: str) -> List[str]:
        """Extract key decisions made during the meeting."""
        prompt = f"""
        Extract all key decisions made during this meeting. Return them as a bulleted list.
        Focus on concrete decisions, not just discussions or suggestions.
        
        Transcript:
        {transcript_text[:2000]}
        
        Key Decisions:
        """
        
        response = self._call_llm(prompt)
        return self._parse_bulleted_list(response)
    
    def _extract_action_items(self, transcript_text: str) -> List[Dict[str, str]]:
        """Extract action items with assignees and deadlines."""
        prompt = f"""
        Extract action items from this meeting transcript. For each action item, identify:
        1. The action to be taken
        2. Who is responsible (if mentioned)
        3. When it should be completed (if mentioned)
        
        Format as a structured list.
        
        Transcript:
        {transcript_text[:2000]}
        
        Action Items:
        """
        
        response = self._call_llm(prompt)
        return self._parse_action_items(response)
    
    def _extract_discussion_highlights(self, transcript_text: str) -> List[str]:
        """Extract key discussion highlights."""
        prompt = f"""
        Identify the most important discussion points from this meeting.
        Focus on topics that had significant debate, important revelations, or critical insights.
        
        Transcript:
        {transcript_text[:2000]}
        
        Discussion Highlights:
        """
        
        response = self._call_llm(prompt)
        return self._parse_bulleted_list(response)
    
    def _summarize_agenda_items(self, agenda_items: List[str]) -> str:
        """Summarize agenda items into a cohesive overview."""
        if not agenda_items:
            return "No specific agenda items identified."
        
        prompt = f"""
        Summarize these agenda items into a cohesive paragraph:
        
        Agenda Items:
        {chr(10).join(f"- {item}" for item in agenda_items)}
        
        Summary:
        """
        
        return self._call_llm(prompt)
    
    def _extract_next_steps(self, transcript_text: str) -> List[str]:
        """Extract next steps and follow-up actions."""
        prompt = f"""
        Extract next steps and follow-up actions from this meeting transcript.
        Focus on concrete actions that need to be taken after the meeting.
        
        Transcript:
        {transcript_text[:2000]}
        
        Next Steps:
        """
        
        response = self._call_llm(prompt)
        return self._parse_bulleted_list(response)
    
    def _call_llm(self, prompt: str) -> str:
        """Call the appropriate LLM with the given prompt."""
        if self.model_name.startswith("gpt") and self.client:
            try:
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=500,
                    temperature=0.3
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                print(f"Error calling OpenAI API: {e}")
                return "Error generating response"
        
        elif self.model_name.startswith("gemini") and self.gemini_model:
            try:
                response = self.gemini_model.generate_content(prompt)
                return response.text.strip()
            except Exception as e:
                print(f"Error calling Gemini API: {e}")
                return "Error generating response"
        
        return "LLM not available"
    
    def _parse_bulleted_list(self, text: str) -> List[str]:
        """Parse bulleted list from LLM response."""
        lines = text.split('\n')
        items = []
        
        for line in lines:
            line = line.strip()
            if line and (line.startswith('-') or line.startswith('•') or line.startswith('*')):
                # Remove bullet point and clean up
                item = re.sub(r'^[-•*]\s*', '', line)
                if item:
                    items.append(item)
        
        return items
    
    def _parse_action_items(self, text: str) -> List[Dict[str, str]]:
        """Parse action items from LLM response."""
        action_items = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if line and (line.startswith('-') or line.startswith('•') or line.startswith('*')):
                # Try to extract structured information
                item_text = re.sub(r'^[-•*]\s*', '', line)
                
                # Simple parsing - in a real implementation, you'd want more sophisticated parsing
                action_item = {
                    "action": item_text,
                    "assignee": "TBD",
                    "deadline": "TBD"
                }
                
                # Try to extract assignee and deadline using simple patterns
                if "assigned to" in item_text.lower():
                    assignee_match = re.search(r"assigned to ([^,]+)", item_text, re.IGNORECASE)
                    if assignee_match:
                        action_item["assignee"] = assignee_match.group(1).strip()
                
                if "by" in item_text.lower() or "deadline" in item_text.lower():
                    deadline_match = re.search(r"(?:by|deadline).*?([^,]+)", item_text, re.IGNORECASE)
                    if deadline_match:
                        action_item["deadline"] = deadline_match.group(1).strip()
                
                action_items.append(action_item)
        
        return action_items
    
    def _rule_based_summarization(self, transcript_text: str, processed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback rule-based summarization when LLM is not available."""
        return {
            "meeting_summary": "Meeting summary generated using rule-based approach. LLM integration recommended for better results.",
            "key_decisions": processed_data.get("decisions", []),
            "action_items": [{"action": item, "assignee": "TBD", "deadline": "TBD"} for item in processed_data.get("action_items", [])],
            "discussion_highlights": processed_data.get("key_points", []),
            "agenda_summary": f"Agenda covered: {'; '.join(processed_data.get('agenda_items', []))}",
            "next_steps": processed_data.get("action_items", [])
        }


# Test the summarizer
if __name__ == "__main__":
    sample_transcript = """
    Meeting: Project Planning Session
    Date: 2024-01-15
    Attendees: John, Sarah, Mike, Lisa
    
    John: Welcome everyone. We need to decide on the project timeline today.
    
    Sarah: I think we should complete the backend by end of February.
    
    Mike: Agreed. We also need to assign someone to handle the database design.
    
    Lisa: I can take on the database design. I'll have it ready by February 10th.
    
    John: Perfect. Decision made - Lisa will handle database design by February 10th.
    
    Sarah: For next meeting, we should discuss the testing strategy.
    
    Mike: Also, we need to plan the deployment process.
    
    John: Next meeting scheduled for March 1st.
    """
    
    summarizer = MeetingSummarizer()
    
    # Mock processed data
    processed_data = {
        "agenda_items": ["project timeline", "backend completion"],
        "decisions": ["Lisa assigned to database design by February 10th"],
        "action_items": ["Complete database design"],
        "key_points": ["Timeline discussion", "Resource allocation"]
    }
    
    summary = summarizer.summarize_meeting(sample_transcript, processed_data)
    
    print("Summarized Information:")
    for key, value in summary.items():
        print(f"{key}: {value}")
