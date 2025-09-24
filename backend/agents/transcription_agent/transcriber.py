import os
import subprocess
from pathlib import Path
import whisper

FFMPEG_BIN = os.path.join(os.path.dirname(__file__), "ffmpeg", "bin", "ffmpeg.exe")

def ensure_ffmpeg_in_path():
    if FFMPEG_BIN not in os.environ["PATH"]:
        os.environ["PATH"] += os.pathsep + os.path.dirname(FFMPEG_BIN)

ensure_ffmpeg_in_path()

def split_video_to_chunks(input_path: str, chunk_dir: str, chunk_length: int = 600):
    """
    Split video into smaller segments of `chunk_length` seconds
    """
    Path(chunk_dir).mkdir(parents=True, exist_ok=True)
    command = [
        FFMPEG_BIN,
        "-i", input_path,
        "-c", "copy",
        "-map", "0",
        "-segment_time", str(chunk_length),
        "-f", "segment",
        os.path.join(chunk_dir, "chunk_%03d.mp4")
    ]
    subprocess.run(command, check=True)
    chunks = sorted(Path(chunk_dir).glob("chunk_*.mp4"))
    return [str(c) for c in chunks]

def convert_to_wav(video_path: str, wav_path: str):
    """
    Convert video to WAV (mono, 16kHz)
    """
    command = [
        FFMPEG_BIN,
        "-y",
        "-i", video_path,
        "-ac", "1",
        "-ar", "16000",
        wav_path
    ]
    subprocess.run(command, check=True)
    return wav_path

def transcribe_audio(audio_path: str):
    """
    Transcribe a single WAV file with Whisper
    """
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    return result["text"]

def generate_transcript(video_path: str):
    """
    Generate transcript from video, supports chunking
    """
    base_dir = Path("temp_uploads")
    chunk_dir = base_dir / f"{Path(video_path).stem}_chunks"
    chunks = split_video_to_chunks(video_path, str(chunk_dir))
    
    full_transcript = ""
    for i, chunk in enumerate(chunks):
        wav_path = base_dir / f"{Path(chunk).stem}.wav"
        convert_to_wav(chunk, str(wav_path))
        text = transcribe_audio(str(wav_path))
        full_transcript += f"\n[Chunk {i+1}]\n{text}\n"
        # Clean up WAV
        wav_path.unlink(missing_ok=True)
    
    # Clean up chunks
    for c in Path(chunk_dir).glob("*"):
        c.unlink()
    chunk_dir.rmdir()

    return full_transcript
