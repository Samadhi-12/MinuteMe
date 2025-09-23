"""
Minutes Generator Agent

Automatically generates meeting minutes from text transcripts.
Extracts key points, decisions, and discussion summaries.
"""

from .minutes_generator import MinutesGenerator
from .transcript_processor import TranscriptProcessor
from .summarizer import MeetingSummarizer
from .formatter import MinutesFormatter

__all__ = ['MinutesGenerator', 'TranscriptProcessor', 'MeetingSummarizer', 'MinutesFormatter']
