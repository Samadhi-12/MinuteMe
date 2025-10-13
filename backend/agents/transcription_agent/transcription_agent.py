import os
import json
import time
import google.generativeai as genai
from dotenv import load_dotenv
import gdown  # For downloading from Google Drive

def configure_gemini():
    """
    Configures the Gemini API with the key from environment variables.
    """
    load_dotenv()
    # Corrected to use GOOGLE_API_KEY from your .env file
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables. Please set it in your .env file.")
    genai.configure(api_key=api_key)

def transcribe_video(video_path: str = None, video_url: str = None, output_path: str = "transcript.json"):
    """
    Transcribes a video file using the Gemini model, downloading it if a URL is provided.

    Args:
        video_path (str, optional): The local path to the video file.
        video_url (str, optional): A public URL (e.g., Google Drive) to the video file.
        output_path (str): The path to save the output JSON file.

    Returns:
        str: The generated transcript text, or None if an error occurred.
    """
    if not video_path and not video_url:
        raise ValueError("Either video_path or video_url must be provided.")

    local_video_path = video_path
    is_temp_file = False
    video_file = None

    try:
        # 1. Configure the Gemini API
        configure_gemini()

        # 2. Download the video if a URL is provided
        if video_url:
            print(f"Downloading video from URL: {video_url}")
            # Define a temporary path for the downloaded file
            temp_dir = "data/meeting_video/temp"
            os.makedirs(temp_dir, exist_ok=True)
            local_video_path = os.path.join(temp_dir, "downloaded_video.mp4")
            gdown.download(video_url, local_video_path, quiet=False)
            is_temp_file = True
            print(f"Video downloaded to temporary path: {local_video_path}")

        # 3. Check if the video file exists
        if not os.path.exists(local_video_path):
            print(f"Error: Video file not found at '{local_video_path}'")
            return None

        # 4. Upload the video file to the Gemini API
        print(f"Uploading video: {local_video_path}...")
        video_file = genai.upload_file(path=local_video_path, display_name="Meeting Video")
        print(f"Completed upload: {video_file.uri}")

        # 5. Wait for the video to be processed
        while video_file.state.name == "PROCESSING":
            print("Waiting for video to be processed...")
            time.sleep(10)
            video_file = genai.get_file(video_file.name)

        if video_file.state.name == "FAILED":
            print("Video processing failed.")
            return None

        # 6. Instantiate the model and generate the transcript with speaker labels
        print("Generating transcription with speaker labels...")
        model = genai.GenerativeModel(model_name="gemini-2.5-flash")

        # Updated prompt to request speaker diarization
        prompt = "Transcribe the audio from this video. Include speaker labels (diarization) for each part of the conversation. For example: 'Speaker 1: Hello there. Speaker 2: Hi, how are you?'"

        # 7. Send the prompt and video file to the model
        response = model.generate_content([prompt, video_file], request_options={"timeout": 600})

        # 8. Extract and print the transcript
        transcript = response.text
        print("\n--- Transcription ---")
        print(transcript)
        print("---------------------\n")

        # 9. Save the transcript to a JSON file
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        output_data = {"transcript": transcript}
        with open(output_path, 'w') as f:
            json.dump(output_data, f, indent=2)
        print(f"Transcript saved to {output_path}")

        return transcript

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        # 10. Clean up uploaded and temporary files
        if video_file:
            print(f"Deleting uploaded file from Gemini service: {video_file.name}")
            genai.delete_file(video_file.name)
        if is_temp_file and local_video_path and os.path.exists(local_video_path):
            print(f"Deleting temporary local file: {local_video_path}")
            os.remove(local_video_path)


if __name__ == '__main__':
    # --- How to use this script ---
    # 1. Make sure you have a .env file in the `backend` directory with your GOOGLE_API_KEY.
    # 2. Provide either a local video file path OR a public Google Drive URL.

    # --- Example with a local file ---
    # video_file_path = "data/meeting_video/meeting.mp4"
    # video_drive_url = None

    # --- Example with a Google Drive URL ---
    # Make sure the link is public / shareable
    video_file_path = None
    video_drive_url = "https://drive.google.com/file/d/1-sample-id-for-a-video/view?usp=sharing" # Replace with a real public video link

    # Define the output path for the transcript
    output_file_path = "data/transcript_meeting/transcript_meeting.json"

    # Call the transcription function
    transcribe_video(video_path=video_file_path, video_url=video_drive_url, output_path=output_file_path)