from gtts import gTTS
import os
import base64

def generate_audio(text, language_code, filepath):
    tts = gTTS(text=text, lang=language_code)
    tts.save(filepath)

def audio_base64(filepath):
    with open(filepath, "rb") as f:
        audio_base64 = base64.b64encode(f.read()).decode("utf-8")
    return audio_base64

def build_file_path(note_id, audio_folder):
    safe_filename = f"{note_id}.mp3"
    filepath = os.path.join(audio_folder, safe_filename)
    return filepath
