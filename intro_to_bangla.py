import avro
import os


import audio
import anki
import create_note

# Declare Constants
DECK_NAME = "Intro to  Bangla"
SENTENCE_FIELD = "Sentence"        
AUDIO_FIELD = "Audio"  
ROMANIZATION_FIELD = "Romanization"  
TRANSLATION_FIELD = "Translation"

ADD_TRANSLATION_CARD_FIELD = "TranslationPrompt"
TRANSLATION_NOTE_ID_FIELD = "TranslationID"

LANGUAGE_CODE = "bn" 
AUDIO_FOLDER = "bangla_audio"

# Create audio folder if it doesn't exist
os.makedirs(AUDIO_FOLDER, exist_ok=True)


def add_audio():
    note_ids = anki.get_model_note_ids(DECK_NAME, "BanglaCloze")
    for note_id in note_ids:
        note_audio = anki.get_note_field_value(note_id, AUDIO_FIELD)
        if note_audio != "":
            print(note_audio)
            print(f"Audio already exists for note {note_id}")
            continue
        sentence = anki.get_note_field_value(note_id, SENTENCE_FIELD)
        path = audio.build_file_path(note_id, AUDIO_FOLDER)
        audio.generate_audio(sentence, LANGUAGE_CODE, path)
        anki.store_audio_file(path)
        anki.add_audio_to_note_field(note_id, path, AUDIO_FIELD)

def add_automatic_transliteration():
    DECK_NAME = "Intro to  Bangla"
    SOURCE_FIELD = "Sentence"
    TARGET_FIELD = "Romanization"
    note_ids = anki.get_model_note_ids(DECK_NAME, "BanglaCloze")
    for note_id in note_ids:
        romanization = anki.get_note_field_value(note_id, ROMANIZATION_FIELD)
        if romanization != "":
            print(f"Romanization already exists for note {note_id}")
            print(romanization)
            continue
        else:
            sentence = anki.get_note_field_value(note_id, SENTENCE_FIELD)
            transliterated_sentence = avro.reverse(sentence)
            anki.add_value_to_note_field(note_id, transliterated_sentence, ROMANIZATION_FIELD)

def create_translation_cards():
    note_ids = anki.get_model_note_ids(DECK_NAME, "BanglaCloze")
    for note_id in note_ids:
        add_translation_card = anki.get_note_field_value(note_id, ADD_TRANSLATION_CARD_FIELD)
        translation_note_id = anki.get_note_field_value(note_id, TRANSLATION_NOTE_ID_FIELD)
        
        if add_translation_card == "1" and translation_note_id == "":
            sentence = anki.get_note_field_value(note_id, SENTENCE_FIELD)
            romanization = anki.get_note_field_value(note_id, ROMANIZATION_FIELD)
            translation = anki.get_note_field_value(note_id, TRANSLATION_FIELD)
            audio = anki.get_note_field_value(note_id, AUDIO_FIELD)
            tags = anki.get_note_tags(note_id)

            response = create_note.create_translation_note(DECK_NAME, {"translation": translation, "sentence": sentence, "romanization": romanization, "audio": audio, "source_note_id": note_id, "tags": tags})

def main():
    add_audio()
    add_automatic_transliteration()
    create_translation_cards()

if __name__ == "__main__":
    main()