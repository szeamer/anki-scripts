import avro
import os 

import audio
import anki
import create_note

DECK_NAME = "Colloquial Norwegian"
SENTENCE_FIELD = "Sentence"
AUDIO_FIELD = "Audio"
TRANSLATION_FIELD = "Translation"

ADD_TRANSLATION_CARD_FIELD = "TranslationPrompt"
TRANSLATION_NOTE_ID_FIELD = "TranslationID"

LANGUAGE_CODE = "no"
AUDIO_FOLDER = "norsk_audio"

os.makedirs(AUDIO_FOLDER, exist_ok=True)

def add_audio():
    note_ids = anki.get_model_note_ids(DECK_NAME, "CustomCloze")
    for note_id in note_ids:
        note_audio = anki.get_note_field_value(note_id, AUDIO_FIELD)
        if note_audio != "":
            print(f"Audio already exists for note {note_id}")
            continue
        sentence = anki.get_note_field_value(note_id, SENTENCE_FIELD)
        path = audio.build_file_path(note_id, AUDIO_FOLDER)
        audio.generate_audio(sentence, LANGUAGE_CODE, path)
        anki.store_audio_file(path)
        anki.add_audio_to_note_field(note_id, path, AUDIO_FIELD)
        print(f"Added audio to note {note_id}")

def create_translation_cards():
    note_ids = anki.get_model_note_ids(DECK_NAME, "CustomCloze")
    for note_id in note_ids:
        add_translation_card = anki.get_note_field_value(note_id, ADD_TRANSLATION_CARD_FIELD)
        translation_note_id = anki.get_note_field_value(note_id, TRANSLATION_NOTE_ID_FIELD)
        
        if add_translation_card == "1" and translation_note_id == "":
            sentence = anki.get_note_field_value(note_id, SENTENCE_FIELD)
            translation = anki.get_note_field_value(note_id, TRANSLATION_FIELD)
            audio = anki.get_note_field_value(note_id, AUDIO_FIELD)
            tags = anki.get_note_tags(note_id)

            response = create_note.create_translation_note(DECK_NAME, {"translation": translation, "sentence": sentence, "audio": audio, "source_note_id": note_id, "tags": tags})


def main():
    add_audio()
    create_translation_cards()

if __name__ == "__main__":
    main()