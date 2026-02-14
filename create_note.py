import anki

def create_translation_note(
    deck_name,
    fields_dict
):
    """
    Creates a new note in Anki of model 'Type Translation'.

    Parameters:
        deck_name (str): Target deck
        fields_dict (dict): Dictionary with the following keys: sentence, translation, romanization, audio, source_note_id
            sentence (str): Content for Sentence field
            translation (str): Content for Translation field
            romanization (str): Content for Romanization field
            audio (str): Content for Audio field
            source_note_id (int): ID of source cloze note

    Returns:
        int: The newly created note ID
    """

    note = {
        "deckName": deck_name,
        "modelName": "TypeTranslation",
        "fields": {
            "Sentence": fields_dict["sentence"],
            "Translation": fields_dict["translation"],
            "Romanization": fields_dict["romanization"],
            "Audio": fields_dict["audio"],
            "NoteID": str(fields_dict["source_note_id"])
        },
        "options": {
            "allowDuplicate": False
        },
        "tags": ["auto_generated", "translation"] + fields_dict["tags"]
    }

    response = anki.anki_request("addNote", note=note)

    new_note_id = response["result"]

    anki.anki_request(
        "updateNoteFields",
        note={
            "id": fields_dict["source_note_id"],
            "fields": {
                "TranslationID": str(new_note_id)
            }
        }
    )

    print(f"Created translation card for note {fields_dict['source_note_id']}: {new_note_id}")
    return response