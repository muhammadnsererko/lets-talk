import pyttsx3
import tempfile
import os
from dotenv import load_dotenv
import re

load_dotenv()

"""
Service for integrating with AWS Polly to synthesize speech from text.
Includes a mock for local testing and error handling.
"""

"""
Voice module plugin interface and pyttsx3 implementation for plug-and-play support, now with SSML-like and adaptive features.
"""

class VoiceModuleBase:
    def synthesize(self, text, voice_id=None, output_format="mp3", rate=None, volume=None, ssml=None):
        raise NotImplementedError("Voice modules must implement the synthesize method.")

class Pyttsx3VoiceModule(VoiceModuleBase):
    def synthesize(self, text, voice_id=None, output_format="mp3", rate=None, volume=None, ssml=None):
        engine = pyttsx3.init()
        # Apply voice
        if voice_id:
            voices = engine.getProperty('voices')
            for v in voices:
                if voice_id in v.id:
                    engine.setProperty('voice', v.id)
                    break
        # Adaptive rate and volume
        if rate is not None:
            engine.setProperty('rate', rate)
        if volume is not None:
            engine.setProperty('volume', volume)
        # SSML-like support: parse <break>, <emphasis>, <prosody> tags
        parsed_text = self._parse_ssml(text if ssml is None else ssml)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tf:
            temp_path = tf.name
        try:
            engine.save_to_file(parsed_text, temp_path)
            engine.runAndWait()
            with open(temp_path, "rb") as f:
                audio_data = f.read()
        finally:
            os.remove(temp_path)
        return {"OutputFormat": output_format, "AudioStream": audio_data}
    def _parse_ssml(self, text):
        # Replace <break time="Xms"/> with appropriate pauses
        text = re.sub(r'<break time="(\d+)ms"\s*/>', lambda m: ' ' * (int(m.group(1)) // 250), text)
        # Replace <emphasis>...</emphasis> with uppercase
        text = re.sub(r'<emphasis>(.*?)</emphasis>', lambda m: m.group(1).upper(), text)
        # Replace <prosody rate="slow">...</prosody> with slow marker
        text = re.sub(r'<prosody rate="slow">(.*?)</prosody>', lambda m: '[SLOW] ' + m.group(1), text)
        # Replace <prosody rate="fast">...</prosody> with fast marker
        text = re.sub(r'<prosody rate="fast">(.*?)</prosody>', lambda m: '[FAST] ' + m.group(1), text)
        # Replace <prosody volume="loud">...</prosody> with loud marker
        text = re.sub(r'<prosody volume="loud">(.*?)</prosody>', lambda m: '[LOUD] ' + m.group(1), text)
        # Replace <prosody volume="soft">...</prosody> with soft marker
        text = re.sub(r'<prosody volume="soft">(.*?)</prosody>', lambda m: '[SOFT] ' + m.group(1), text)
        return text

# Plugin registry for voice modules
VOICE_MODULES = {}

def register_voice_module(name, module):
    VOICE_MODULES[name] = module

def get_voice_module(name):
    return VOICE_MODULES.get(name)

# Register the default pyttsx3 voice module
register_voice_module("pyttsx3", Pyttsx3VoiceModule())

# Default synthesize_speech function using the selected voice module
DEFAULT_VOICE_MODULE = "pyttsx3"

def synthesize_speech(text, voice_id=None, output_format="mp3", module_name=None, rate=None, volume=None, ssml=None):
    module = get_voice_module(module_name or DEFAULT_VOICE_MODULE)
    if not module:
        return {"error": f"Voice module '{module_name}' not found."}
    try:
        return module.synthesize(text, voice_id=voice_id, output_format=output_format, rate=rate, volume=volume, ssml=ssml)
    except Exception as e:
        return {"error": str(e)}