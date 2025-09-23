"""
Minutes Formatter for creating structured meeting minutes documents.
Formats minutes with date, attendees, agenda items, and discussion points.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime


class MinutesFormatter:
    """
    Formats processed and summarized data into structured meeting minutes.
    
    Creates well-organized minutes with:
    - Meeting metadata (date, attendees, agenda items)
    - Discussion points and key outcomes
    - Decisions and action items
    - Next steps and follow-ups
    """
    
    def __init__(self):
        """Initialize the formatter."""
        pass
    
    def format_minutes(
        self,
        processed_data: Dict[str, Any],
        summary_data: Dict[str, Any],
        meeting_id: Optional[str] = None,
        meeting_metadata: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Format processed and summarized data into structured minutes.
        
        Args:
            processed_data: Data processed by TranscriptProcessor
            summary_data: Data summarized by MeetingSummarizer
            meeting_id: Optional meeting identifier
            meeting_metadata: Optional additional metadata
            
        Returns:
            Dictionary containing formatted meeting minutes
        """
        # Generate meeting ID if not provided
        if not meeting_id:
            meeting_id = f"meeting_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Format the minutes document
        minutes = {
            "meeting_id": meeting_id,
            "meeting_date": processed_data.get("meeting_date") or datetime.now().strftime("%Y-%m-%d"),
            "attendees": processed_data.get("attendees", []),
            "meeting_summary": summary_data.get("meeting_summary", ""),
            
            # Agenda and discussion points
            "agenda_items": processed_data.get("agenda_items", []),
            "agenda_summary": summary_data.get("agenda_summary", ""),
            "discussion_highlights": summary_data.get("discussion_highlights", []),
            
            # Key outcomes
            "key_decisions": summary_data.get("key_decisions", []),
            "action_items": summary_data.get("action_items", []),
            "next_steps": summary_data.get("next_steps", []),
            
            # Detailed information
            "decisions": processed_data.get("decisions", []),
            "deadlines": processed_data.get("deadlines", []),
            "key_points": processed_data.get("key_points", []),
            
            # Metadata
            "generated_at": datetime.now().isoformat(),
            "generation_method": "Minutes Generator Agent",
            "additional_metadata": meeting_metadata or {}
        }
        
        return minutes
    
    def format_minutes_as_text(self, minutes: Dict[str, Any]) -> str:
        """
        Format minutes as a readable text document.
        
        Args:
            minutes: Structured minutes dictionary
            
        Returns:
            Formatted text document
        """
        text_doc = []
        
        # Header
        text_doc.append("=" * 60)
        text_doc.append("MEETING MINUTES")
        text_doc.append("=" * 60)
        text_doc.append("")
        
        # Meeting Information
        text_doc.append("MEETING INFORMATION")
        text_doc.append("-" * 20)
        text_doc.append(f"Meeting ID: {minutes.get('meeting_id', 'N/A')}")
        text_doc.append(f"Date: {minutes.get('meeting_date', 'N/A')}")
        text_doc.append(f"Attendees: {', '.join(minutes.get('attendees', []))}")
        text_doc.append("")
        
        # Meeting Summary
        if minutes.get('meeting_summary'):
            text_doc.append("MEETING SUMMARY")
            text_doc.append("-" * 15)
            text_doc.append(minutes['meeting_summary'])
            text_doc.append("")
        
        # Agenda Items
        if minutes.get('agenda_items'):
            text_doc.append("AGENDA ITEMS")
            text_doc.append("-" * 12)
            for i, item in enumerate(minutes['agenda_items'], 1):
                text_doc.append(f"{i}. {item}")
            text_doc.append("")
            
            # Agenda Summary
            if minutes.get('agenda_summary'):
                text_doc.append("Agenda Summary:")
                text_doc.append(minutes['agenda_summary'])
                text_doc.append("")
        
        # Discussion Highlights
        if minutes.get('discussion_highlights'):
            text_doc.append("DISCUSSION HIGHLIGHTS")
            text_doc.append("-" * 21)
            for i, highlight in enumerate(minutes['discussion_highlights'], 1):
                text_doc.append(f"{i}. {highlight}")
            text_doc.append("")
        
        # Key Decisions
        if minutes.get('key_decisions'):
            text_doc.append("KEY DECISIONS")
            text_doc.append("-" * 14)
            for i, decision in enumerate(minutes['key_decisions'], 1):
                text_doc.append(f"{i}. {decision}")
            text_doc.append("")
        
        # Action Items
        if minutes.get('action_items'):
            text_doc.append("ACTION ITEMS")
            text_doc.append("-" * 12)
            for i, item in enumerate(minutes['action_items'], 1):
                if isinstance(item, dict):
                    text_doc.append(f"{i}. {item.get('action', 'N/A')}")
                    if item.get('assignee') and item['assignee'] != 'TBD':
                        text_doc.append(f"   Assigned to: {item['assignee']}")
                    if item.get('deadline') and item['deadline'] != 'TBD':
                        text_doc.append(f"   Deadline: {item['deadline']}")
                else:
                    text_doc.append(f"{i}. {item}")
            text_doc.append("")
        
        # Next Steps
        if minutes.get('next_steps'):
            text_doc.append("NEXT STEPS")
            text_doc.append("-" * 10)
            for i, step in enumerate(minutes['next_steps'], 1):
                text_doc.append(f"{i}. {step}")
            text_doc.append("")
        
        # Footer
        text_doc.append("=" * 60)
        text_doc.append(f"Generated on: {minutes.get('generated_at', 'N/A')}")
        text_doc.append(f"Generated by: {minutes.get('generation_method', 'N/A')}")
        text_doc.append("=" * 60)
        
        return "\n".join(text_doc)
    
    def format_minutes_as_html(self, minutes: Dict[str, Any]) -> str:
        """
        Format minutes as an HTML document.
        
        Args:
            minutes: Structured minutes dictionary
            
        Returns:
            Formatted HTML document
        """
        html_doc = []
        
        # HTML header
        html_doc.append("<!DOCTYPE html>")
        html_doc.append("<html lang='en'>")
        html_doc.append("<head>")
        html_doc.append("    <meta charset='UTF-8'>")
        html_doc.append("    <meta name='viewport' content='width=device-width, initial-scale=1.0'>")
        html_doc.append("    <title>Meeting Minutes</title>")
        html_doc.append("    <style>")
        html_doc.append("        body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }")
        html_doc.append("        h1 { color: #333; border-bottom: 2px solid #333; padding-bottom: 10px; }")
        html_doc.append("        h2 { color: #666; border-bottom: 1px solid #ccc; padding-bottom: 5px; }")
        html_doc.append("        .metadata { background-color: #f5f5f5; padding: 15px; border-radius: 5px; }")
        html_doc.append("        ul { margin: 10px 0; }")
        html_doc.append("        li { margin: 5px 0; }")
        html_doc.append("        .action-item { background-color: #e8f4fd; padding: 10px; margin: 5px 0; border-radius: 3px; }")
        html_doc.append("        .footer { margin-top: 30px; padding-top: 20px; border-top: 1px solid #ccc; font-size: 0.9em; color: #666; }")
        html_doc.append("    </style>")
        html_doc.append("</head>")
        html_doc.append("<body>")
        
        # Title
        html_doc.append("    <h1>Meeting Minutes</h1>")
        
        # Meeting Information
        html_doc.append("    <div class='metadata'>")
        html_doc.append(f"        <strong>Meeting ID:</strong> {minutes.get('meeting_id', 'N/A')}<br>")
        html_doc.append(f"        <strong>Date:</strong> {minutes.get('meeting_date', 'N/A')}<br>")
        html_doc.append(f"        <strong>Attendees:</strong> {', '.join(minutes.get('attendees', []))}")
        html_doc.append("    </div>")
        html_doc.append("")
        
        # Meeting Summary
        if minutes.get('meeting_summary'):
            html_doc.append("    <h2>Meeting Summary</h2>")
            html_doc.append(f"    <p>{minutes['meeting_summary']}</p>")
            html_doc.append("")
        
        # Agenda Items
        if minutes.get('agenda_items'):
            html_doc.append("    <h2>Agenda Items</h2>")
            html_doc.append("    <ul>")
            for item in minutes['agenda_items']:
                html_doc.append(f"        <li>{item}</li>")
            html_doc.append("    </ul>")
            html_doc.append("")
            
            if minutes.get('agenda_summary'):
                html_doc.append("    <h3>Agenda Summary</h3>")
                html_doc.append(f"    <p>{minutes['agenda_summary']}</p>")
                html_doc.append("")
        
        # Discussion Highlights
        if minutes.get('discussion_highlights'):
            html_doc.append("    <h2>Discussion Highlights</h2>")
            html_doc.append("    <ul>")
            for highlight in minutes['discussion_highlights']:
                html_doc.append(f"        <li>{highlight}</li>")
            html_doc.append("    </ul>")
            html_doc.append("")
        
        # Key Decisions
        if minutes.get('key_decisions'):
            html_doc.append("    <h2>Key Decisions</h2>")
            html_doc.append("    <ul>")
            for decision in minutes['key_decisions']:
                html_doc.append(f"        <li>{decision}</li>")
            html_doc.append("    </ul>")
            html_doc.append("")
        
        # Action Items
        if minutes.get('action_items'):
            html_doc.append("    <h2>Action Items</h2>")
            for item in minutes['action_items']:
                if isinstance(item, dict):
                    html_doc.append("    <div class='action-item'>")
                    html_doc.append(f"        <strong>{item.get('action', 'N/A')}</strong><br>")
                    if item.get('assignee') and item['assignee'] != 'TBD':
                        html_doc.append(f"        Assigned to: {item['assignee']}<br>")
                    if item.get('deadline') and item['deadline'] != 'TBD':
                        html_doc.append(f"        Deadline: {item['deadline']}")
                    html_doc.append("    </div>")
                else:
                    html_doc.append(f"    <div class='action-item'>{item}</div>")
            html_doc.append("")
        
        # Next Steps
        if minutes.get('next_steps'):
            html_doc.append("    <h2>Next Steps</h2>")
            html_doc.append("    <ul>")
            for step in minutes['next_steps']:
                html_doc.append(f"        <li>{step}</li>")
            html_doc.append("    </ul>")
            html_doc.append("")
        
        # Footer
        html_doc.append("    <div class='footer'>")
        html_doc.append(f"        Generated on: {minutes.get('generated_at', 'N/A')}<br>")
        html_doc.append(f"        Generated by: {minutes.get('generation_method', 'N/A')}")
        html_doc.append("    </div>")
        
        # Close HTML
        html_doc.append("</body>")
        html_doc.append("</html>")
        
        return "\n".join(html_doc)


# Test the formatter
if __name__ == "__main__":
    # Sample data
    processed_data = {
        "attendees": ["John", "Sarah", "Mike", "Lisa"],
        "meeting_date": "2024-01-15",
        "agenda_items": ["project status", "timeline discussion"],
        "decisions": ["Lisa assigned to database design"],
        "key_points": ["Timeline discussion", "Resource allocation"]
    }
    
    summary_data = {
        "meeting_summary": "Project planning meeting focused on timeline and resource allocation.",
        "key_decisions": ["Lisa will handle database design by February 10th"],
        "action_items": [{"action": "Complete database design", "assignee": "Lisa", "deadline": "February 10th"}],
        "discussion_highlights": ["Timeline discussion", "Resource allocation"],
        "agenda_summary": "Discussion focused on current project status and timeline planning.",
        "next_steps": ["Complete database design", "Schedule next meeting"]
    }
    
    formatter = MinutesFormatter()
    minutes = formatter.format_minutes(processed_data, summary_data, "test_001")
    
    print("Formatted Minutes (JSON):")
    import json
    print(json.dumps(minutes, indent=2))
    
    print("\n" + "="*60)
    print("Formatted Minutes (Text):")
    print(formatter.format_minutes_as_text(minutes))
