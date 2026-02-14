import requests
import json
import re
import html
import audio


ANKI_CONNECT_URL = "http://localhost:8765"  # Change if different   

def anki_request(action, **params):
    """
    Sends a request to the AnkiConnect API.

    Args:
        action (str): The action to perform.
        **params: Additional parameters to send with the request.

    Returns:
        dict: The response from the AnkiConnect API.
    """
    return requests.post(
        ANKI_CONNECT_URL,
        json={
            "action": action,
            "version": 6,
            "params": params
        }
    ).json()

def get_note_ids(deck_name):
    """
    Takes the name of a deck and returns a list of integer note IDs.
    """
    query = f'deck:"{deck_name}"'
    response = anki_request("findNotes", query=query)
    note_ids = response["result"]

    print(f"Found {len(note_ids)} notes.")
    return note_ids

def get_model_note_ids(deck_name, model_name):
    """
    Takes the name of a deck and a model name and returns a list of integer note IDs.
    """
    query = f"deck:\"{deck_name}\" note:{model_name}"
    response = anki_request("findNotes", query=query)
    note_ids = response["result"]

    print(f"Found {len(note_ids)} notes.")
    return note_ids

def get_note_field_value(note_id, field_name):
    """
    Takes the ID of a note and the name of a field and returns the value of the field.
    """
    note_info = anki_request("notesInfo", notes=[note_id])["result"][0]

    if field_name == "Audio":
        return note_info["fields"][field_name]["value"]
    else:
        text = note_info["fields"][field_name]["value"].strip()
        text = clean_cloze(text)
        text = clean_anki_html(text)
        return text

def get_note_tags(note_id):
    note_info = anki_request("notesInfo", notes=[note_id])["result"][0]
    return note_info["tags"]

def add_audio_to_note_field(note_id, filepath, field_name):
    value = audio.audio_base64(filepath)
    audio_tag = f"[sound:{filepath}]"
    add_value_to_note_field(note_id, audio_tag, field_name)

def add_value_to_note_field(note_id, value, field_name):
    result = anki_request(
        "updateNoteFields",
        note={
            "id": note_id,
            "fields": {
                field_name: value
            }
        }
    )
    print(result)

    print(f"Added audio to note {note_id}")

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

def clean_cloze(sentence):
    """
    Replaces segments like {{c1::ducks::kacsa}} with 'ducks'
    Also works if there is no hint: {{c1::ducks}}. In the case of no cloze, returns the original sentence.
    """
    pattern = r"\{\{c\d+::([^}:]+)(?:::[^}]*)?\}\}"
    return re.sub(pattern, r"\1", sentence)

def store_audio_file(filepath):
    value = audio.audio_base64(filepath)
    anki_request(
        "storeMediaFile",
        filename=filepath,
        data=value
    )