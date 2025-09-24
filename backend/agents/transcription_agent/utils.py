import os
from pathlib import Path

def ensure_dir(path: str):
    """
    Ensure a directory exists
    """
    Path(path).mkdir(parents=True, exist_ok=True)
