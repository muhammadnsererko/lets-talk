import pyttsx3
import tempfile
import os
from dotenv import load_dotenv
import boto3

load_dotenv()

"""
Service for integrating with AWS Polly to synthesize speech from text.
Includes a mock for local testing and error handling.
"""

def synthesize_speech(text, voice_id=None, output_format="mp3"):
    """
    Synthesize speech from the provided text using pyttsx3 (offline TTS).
    """
    engine = pyttsx3.init()
    # Optionally set voice by voice_id if needed
    if voice_id:
        voices = engine.getProperty('voices')
        for v in voices:
            if voice_id in v.id:
                engine.setProperty('voice', v.id)
                break
    # Use a temporary file to store the output
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tf:
        temp_path = tf.name
    try:
        engine.save_to_file(text, temp_path)
        engine.runAndWait()
        with open(temp_path, "rb") as f:
            audio_data = f.read()
    finally:
        os.remove(temp_path)
    return {"OutputFormat": output_format, "AudioStream": audio_data}
    try:
        # Mock for local testing
        print(f"Simulating Polly: Speaking '{text}'")
        return {"OutputFormat": "mp3", "AudioStream": "mocked_audio"}

        # Uncomment for real AWS Polly integration:
        # polly = boto3.client(
        #     'polly',
        #     region_name=os.getenv('AWS_REGION', 'us-east-1'),
        #     aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        #     aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        # )
        # response = polly.synthesize_speech(
        #     Text=text, OutputFormat='mp3', VoiceId='Joanna'
        # )
        # return response
    except Exception as e:
        return {"error": str(e)}