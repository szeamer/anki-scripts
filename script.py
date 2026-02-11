import requests
import json
import os
import re
from gtts import gTTS
import html
import base64

ANKI_CONNECT_URL = "http://localhost:8765"  # Change if different   

def anki_request(action, **params):
    return requests.post(
        ANKI_CONNECT_URL,
        json={
            "action": action,
            "version": 6,
            "params": params
        }
    ).json()

print(anki_request("deckNames"))

def clean_anki_html(text):
    """
    - Converts HTML entities like &nbsp; to real characters
    - Removes HTML tags
    - Normalizes whitespace
    """

    text = html.unescape(text)

    text = re.sub(r"<.*?>", "", text)

    text = text.replace("\xa0", " ")

    text = re.sub(r"\s+", " ", text)

    return text.strip()

def clean_sentence(sentence):
    """
    Replaces segments like {{c1::ducks::kacsa}} with 'ducks'
    Also works if there is no hint: {{c1::ducks}}
    """
    pattern = r"\{\{c\d+::([^}:]+)(?:::[^}]*)?\}\}"
    return re.sub(pattern, r"\1", sentence)

def get_note_ids(deck_name):
    # 1️⃣ Get all notes from the deck
    query = f'deck:"{deck_name}"'
    response = anki_request("findNotes", query=query)
    note_ids = response["result"]

    print(f"Found {len(note_ids)} notes.")
    return note_ids

def get_field_value(note_id, field_name):
    note_info = anki_request("notesInfo", notes=[note_id])["result"][0]

    text = note_info["fields"][field_name]["value"].strip()
    text = clean_sentence(text)
    text = clean_anki_html(text)

    return text

def build_file_path(note_id, audio_folder):
    safe_filename = f"{note_id}.mp3"
    filepath = os.path.join(audio_folder, safe_filename)
    return filepath

def generate_audio(text, language_code, filepath):
    # 4️⃣ Generate TTS audio
    tts = gTTS(text=text, lang=language_code)
    tts.save(filepath)

def audio_base64(filepath):
    with open(filepath, "rb") as f:
        audio_base64 = base64.b64encode(f.read()).decode("utf-8")
    return audio_base64

def store_audio_file(filepath):
    value = audio_base64(filepath)
    anki_request(
        "storeMediaFile",
        filename=filepath,
        data=value
    )

def add_audio_to_field(note_id, filepath, field_name):
    value = audio_base64(filepath)
    audio_tag = f"[sound:{filepath}]"
    add_value_to_field(note_id, audio_tag, field_name)

def add_value_to_field(note_id, value, field_name):
    anki_request(
        "updateNoteFields",
        note={
            "id": note_id,
            "fields": {
                field_name: value
            }
        }
    )

    print(f"Added audio to note {note_id}")

def add_audio_to_bangla():
    DECK_NAME = "Intro to  Bangla"
    SOURCE_FIELD = "Sentence"        # Field that contains Bangla text
    TARGET_FIELD = "Audio"        # Field where audio should be inserted
    LANGUAGE_CODE = "bn"             # Bangla language code

    # Folder to temporarily store audio files
    AUDIO_FOLDER = "generated_audio"

    # Create audio folder if it doesn't exist
    os.makedirs(AUDIO_FOLDER, exist_ok=True)
    note_ids = get_note_ids(DECK_NAME)
    for note_id in note_ids:
        sentence = get_field_value(note_id, SOURCE_FIELD)
        path = build_file_path(note_id, AUDIO_FOLDER)
        generate_audio(sentence, LANGUAGE_CODE, path)
        store_audio_file(path)
        add_audio_to_field(note_id, path, TARGET_FIELD)

add_audio_to_bangla()
print("Done!")
