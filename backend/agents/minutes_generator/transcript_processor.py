"""
Transcript Processor for extracting key information from meeting transcripts.
Uses NLP techniques including NER for decisions, deadlines, and names.
"""

import re
import spacy
import nltk
from typing import Dict, List, Optional, Any
from datetime import datetime
import dateparser
from collections import defaultdict

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger')


class TranscriptProcessor:
    """
    Processes meeting transcripts to extract key information using NLP techniques.
    
    Key extractions:
    - Attendees and participants
    - Meeting date and time
    - Agenda items and topics
    - Decisions made
    - Deadlines and action items
    - Key discussion points
    """
    
    def __init__(self):
        """Initialize the processor with NLP models."""
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("⚠️ spaCy English model not found. Please install with: python -m spacy download en_core_web_sm")
            self.nlp = None
        
        # Keywords for identifying different types of content
        self.decision_keywords = [
            "decide", "decision", "agree", "approved", "agreed", "conclusion",
            "we will", "we should", "let's", "action item", "resolved"
        ]
        
        self.deadline_keywords = [
            "deadline", "due", "by", "until", "before", "complete by",
            "finish by", "deliver by", "ready by"
        ]
        
        self.action_keywords = [
            "action", "task", "todo", "assign", "responsible", "owner",
            "follow up", "next steps", "will do", "need to"
        ]
    
    def process_transcript(self, transcript_text: str) -> Dict[str, Any]:
        """
        Process transcript to extract key information.
        
        Args:
            transcript_text: Raw transcript text
            
        Returns:
            Dictionary containing extracted information
        """
        if not transcript_text.strip():
            return self._empty_result()
        
        # Clean and preprocess text
        cleaned_text = self._clean_transcript(transcript_text)
        
        # Extract different types of information
        attendees = self._extract_attendees(cleaned_text)
        meeting_date = self._extract_meeting_date(cleaned_text)
        agenda_items = self._extract_agenda_items(cleaned_text)
        decisions = self._extract_decisions(cleaned_text)
        deadlines = self._extract_deadlines(cleaned_text)
        action_items = self._extract_action_items(cleaned_text)
        key_points = self._extract_key_points(cleaned_text)
        
        return {
            "attendees": attendees,
            "meeting_date": meeting_date,
            "agenda_items": agenda_items,
            "decisions": decisions,
            "deadlines": deadlines,
            "action_items": action_items,
            "key_points": key_points,
            "raw_text": cleaned_text
        }
    
    def _clean_transcript(self, text: str) -> str:
        """Clean and normalize transcript text."""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove speaker labels if they exist (e.g., "John:", "Sarah:")
        text = re.sub(r'^[A-Za-z]+:\s*', '', text, flags=re.MULTILINE)
        
        return text.strip()
    
    def _extract_attendees(self, text: str) -> List[str]:
        """Extract meeting attendees using NER and pattern matching."""
        attendees = []
        
        # Look for explicit attendees list
        attendees_pattern = r"attendees?[:\s]+([^.\n]+)"
        matches = re.findall(attendees_pattern, text, re.IGNORECASE)
        
        if matches:
            attendees_str = matches[0]
            attendees = [name.strip() for name in attendees_str.split(',')]
            attendees = [name for name in attendees if name and len(name) > 1]
        
        # If no explicit list, use NER to extract names
        if not attendees and self.nlp:
            doc = self.nlp(text[:2000])  # Process first 2000 chars for performance
            for ent in doc.ents:
                if ent.label_ == "PERSON":
                    attendees.append(ent.text)
        
        return list(set(attendees))  # Remove duplicates
    
    def _extract_meeting_date(self, text: str) -> Optional[str]:
        """Extract meeting date using NER and pattern matching."""
        if self.nlp:
            doc = self.nlp(text[:1000])  # Process first 1000 chars
            
            # Look for DATE entities
            for ent in doc.ents:
                if ent.label_ == "DATE":
                    parsed_date = dateparser.parse(ent.text)
                    if parsed_date:
                        return parsed_date.strftime("%Y-%m-%d")
        
        # Fallback to regex patterns
        date_patterns = [
            r"date[:\s]+(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})",
            r"(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})",
            r"(january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2}(?:st|nd|rd|th)?,?\s+\d{4}"
        ]
        
        for pattern in date_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                date_str = matches[0]
                parsed_date = dateparser.parse(date_str)
                if parsed_date:
                    return parsed_date.strftime("%Y-%m-%d")
        
        return None
    
    def _extract_agenda_items(self, text: str) -> List[str]:
        """Extract agenda items and topics from transcript."""
        agenda_items = []
        
        # Look for agenda-related keywords
        agenda_keywords = [
            "agenda", "topic", "discuss", "review", "plan", "status update",
            "item", "point", "issue"
        ]
        
        sentences = self._split_into_sentences(text)
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            
            # Check if sentence contains agenda-related keywords
            if any(keyword in sentence_lower for keyword in agenda_keywords):
                # Extract the main topic
                topic = self._extract_topic_from_sentence(sentence)
                if topic and len(topic) > 5:
                    agenda_items.append(topic)
        
        return list(set(agenda_items))
    
    def _extract_decisions(self, text: str) -> List[str]:
        """Extract decisions made during the meeting."""
        decisions = []
        sentences = self._split_into_sentences(text)
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            
            # Check if sentence contains decision keywords
            if any(keyword in sentence_lower for keyword in self.decision_keywords):
                decision = self._extract_topic_from_sentence(sentence)
                if decision and len(decision) > 10:
                    decisions.append(decision)
        
        return list(set(decisions))
    
    def _extract_deadlines(self, text: str) -> List[Dict[str, str]]:
        """Extract deadlines and due dates."""
        deadlines = []
        sentences = self._split_into_sentences(text)
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            
            # Check if sentence contains deadline keywords
            if any(keyword in sentence_lower for keyword in self.deadline_keywords):
                # Try to extract deadline information
                deadline_info = self._parse_deadline_sentence(sentence)
                if deadline_info:
                    deadlines.append(deadline_info)
        
        return deadlines
    
    def _extract_action_items(self, text: str) -> List[Dict[str, str]]:
        """Extract action items with assignees."""
        action_items = []
        sentences = self._split_into_sentences(text)
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            
            # Check if sentence contains action keywords
            if any(keyword in sentence_lower for keyword in self.action_keywords):
                action_info = self._parse_action_sentence(sentence)
                if action_info:
                    action_items.append(action_info)
        
        return action_items
    
    def _extract_key_points(self, text: str) -> List[str]:
        """Extract key discussion points."""
        key_points = []
        sentences = self._split_into_sentences(text)
        
        # Look for sentences that seem important
        important_indicators = [
            "important", "critical", "key", "main", "primary", "essential",
            "focus", "priority", "highlight", "note", "remember"
        ]
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            
            if any(indicator in sentence_lower for indicator in important_indicators):
                point = self._extract_topic_from_sentence(sentence)
                if point and len(point) > 10:
                    key_points.append(point)
        
        return list(set(key_points))
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        if self.nlp:
            doc = self.nlp(text)
            return [sent.text.strip() for sent in doc.sents if sent.text.strip()]
        else:
            # Fallback to simple sentence splitting
            sentences = re.split(r'[.!?]+', text)
            return [s.strip() for s in sentences if s.strip()]
    
    def _extract_topic_from_sentence(self, sentence: str) -> str:
        """Extract the main topic from a sentence."""
        # Remove common filler words and clean up
        sentence = re.sub(r'^(let\'s|we\'ll|we should|we need to|we must|i think|i believe)\s*', '', sentence, flags=re.IGNORECASE)
        sentence = re.sub(r'[.!?]+$', '', sentence)
        
        # Extract the main clause (simplified)
        if ':' in sentence:
            sentence = sentence.split(':')[-1]
        
        return sentence.strip()
    
    def _parse_deadline_sentence(self, sentence: str) -> Optional[Dict[str, str]]:
        """Parse deadline information from a sentence."""
        # Simple parsing - in production, use more sophisticated NLP
        deadline_info = {
            "description": sentence.strip(),
            "due_date": "TBD",
            "assignee": "TBD"
        }
        
        # Try to extract date
        if self.nlp:
            doc = self.nlp(sentence)
            for ent in doc.ents:
                if ent.label_ == "DATE":
                    parsed_date = dateparser.parse(ent.text)
                    if parsed_date:
                        deadline_info["due_date"] = parsed_date.strftime("%Y-%m-%d")
                        break
        
        return deadline_info
    
    def _parse_action_sentence(self, sentence: str) -> Optional[Dict[str, str]]:
        """Parse action item information from a sentence."""
        # Simple parsing - in production, use more sophisticated NLP
        action_info = {
            "action": sentence.strip(),
            "assignee": "TBD",
            "due_date": "TBD"
        }
        
        # Try to extract assignee using NER
        if self.nlp:
            doc = self.nlp(sentence)
            for ent in doc.ents:
                if ent.label_ == "PERSON":
                    action_info["assignee"] = ent.text
                    break
        
        return action_info
    
    def _empty_result(self) -> Dict[str, Any]:
        """Return empty result structure."""
        return {
            "attendees": [],
            "meeting_date": None,
            "agenda_items": [],
            "decisions": [],
            "deadlines": [],
            "action_items": [],
            "key_points": [],
            "raw_text": ""
        }


# Test the processor
if __name__ == "__main__":
    sample_transcript = """
    Meeting: Project Planning Session
    Date: 2024-01-15
    Attendees: John Smith, Sarah Johnson, Mike Chen, Lisa Rodriguez
    
    John: Welcome everyone. We need to decide on the project timeline today.
    
    Sarah: We've completed the user interface design. I'll handle the backend development by February 15th.
    
    Mike: I agree. We should also discuss the database schema before we start coding.
    
    Lisa: What about the timeline? We need to set deadlines for the next milestone.
    
    John: Good point. Decision made - backend completion deadline is February 28th.
    
    Sarah: For future discussions, we should plan the testing phase.
    
    Mike: Also, we need to discuss the budget allocation for the third quarter.
    
    Lisa: When should we schedule our next meeting?
    
    John: How about February 15th? That gives us time to complete current tasks.
    """
    
    processor = TranscriptProcessor()
    result = processor.process_transcript(sample_transcript)
    
    print("Processed Information:")
    for key, value in result.items():
        if key != 'raw_text':  # Skip raw text for cleaner output
            print(f"{key}: {value}")
