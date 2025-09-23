"""
Main Minutes Generator class that orchestrates the meeting minutes generation process.
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional, Any

from .transcript_processor import TranscriptProcessor
from .summarizer import MeetingSummarizer
from .formatter import MinutesFormatter


class MinutesGenerator:
    """
    Main class for generating meeting minutes from transcripts.
    
    This class orchestrates the entire process:
    1. Process transcript to extract key information
    2. Summarize discussions and decisions
    3. Format into structured minutes document
    """
    
    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        """
        Initialize the Minutes Generator.
        
        Args:
            model_name: LLM model to use for text processing
        """
        self.model_name = model_name
        self.processor = TranscriptProcessor()
        self.summarizer = MeetingSummarizer(model_name=model_name)
        self.formatter = MinutesFormatter()
        
    def generate_minutes(
        self, 
        transcript_text: str, 
        meeting_id: Optional[str] = None,
        meeting_metadata: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Generate meeting minutes from transcript text.
        
        Args:
            transcript_text: Raw transcript text from the meeting
            meeting_id: Optional meeting identifier
            meeting_metadata: Optional metadata about the meeting
            
        Returns:
            Dictionary containing structured meeting minutes
        """
        print("🔍 Starting minutes generation process...")
        
        # Step 1: Process transcript to extract key information
        print("📝 Processing transcript and extracting key information...")
        processed_data = self.processor.process_transcript(transcript_text)
        
        # Step 2: Summarize discussions and decisions
        print("📊 Summarizing discussions and decisions...")
        summary_data = self.summarizer.summarize_meeting(
            transcript_text, 
            processed_data
        )
        
        # Step 3: Format into structured minutes
        print("📋 Formatting structured minutes...")
        minutes = self.formatter.format_minutes(
            processed_data,
            summary_data,
            meeting_id,
            meeting_metadata
        )
        
        # Step 4: Save minutes
        if meeting_id:
            self._save_minutes(minutes, meeting_id)
        
        print("✅ Minutes generation completed!")
        return minutes
    
    def generate_minutes_from_file(
        self, 
        transcript_file_path: str, 
        meeting_id: Optional[str] = None,
        meeting_metadata: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Generate minutes from a transcript file.
        
        Args:
            transcript_file_path: Path to the transcript file
            meeting_id: Optional meeting identifier
            meeting_metadata: Optional metadata about the meeting
            
        Returns:
            Dictionary containing structured meeting minutes
        """
        try:
            with open(transcript_file_path, 'r', encoding='utf-8') as file:
                transcript_text = file.read()
            
            return self.generate_minutes(transcript_text, meeting_id, meeting_metadata)
        
        except FileNotFoundError:
            raise FileNotFoundError(f"Transcript file not found: {transcript_file_path}")
        except Exception as e:
            raise Exception(f"Error reading transcript file: {str(e)}")
    
    def _save_minutes(self, minutes: Dict[str, Any], meeting_id: str) -> None:
        """Save minutes to file."""
        # Ensure directories exist
        os.makedirs("data/summary", exist_ok=True)
        
        # Save detailed minutes
        minutes_file = f"data/summary/minutes_{meeting_id}.json"
        with open(minutes_file, 'w', encoding='utf-8') as f:
            json.dump(minutes, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Minutes saved to: {minutes_file}")


# Example usage
if __name__ == "__main__":
    # Sample transcript for testing
    sample_transcript = """
    Meeting: Project Planning Session
    Date: 2024-01-15
    Attendees: John Smith, Sarah Johnson, Mike Chen, Lisa Rodriguez
    
    John: Welcome everyone to our project planning session. Let's start with the current status.
    
    Sarah: We've completed the user interface design. The next phase should focus on backend development.
    
    Mike: I agree. We should also discuss the database schema before we start coding.
    
    Lisa: What about the timeline? We need to decide on deadlines for the next milestone.
    
    John: Good point. Let's set the backend completion deadline for February 28th.
    
    Sarah: For future discussions, we should plan the testing phase and deployment strategy.
    
    Mike: Also, we need to discuss the budget allocation for the third quarter.
    
    Lisa: When should we schedule our next meeting?
    
    John: How about February 15th? That gives us time to complete the current tasks.
    
    Sarah: That works for me. We should also prepare the testing framework documentation.
    
    Mike: Agreed. Let's also review the security requirements for the next phase.
    
    Lisa: Perfect. I'll send out the calendar invite for February 15th.
    
    John: Great. Meeting adjourned.
    """
    
    # Initialize generator
    generator = MinutesGenerator()
    
    # Generate minutes
    minutes = generator.generate_minutes(
        sample_transcript, 
        meeting_id="test_001",
        meeting_metadata={"type": "project_planning", "duration": "30 minutes"}
    )
    
    print("\n📋 Generated Minutes:")
    print(json.dumps(minutes, indent=2))
