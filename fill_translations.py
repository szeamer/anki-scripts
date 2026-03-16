from anki import anki_request, clean_anki_html, clean_cloze
from translate import translate_no_en

DECK = "Norsk Subs"
CHUNK = 50


def get_notes_missing_translation():
    query = f'deck:"{DECK}"'
    return anki_request("findNotes", query=query)["result"]


def fetch_notes(ids):
    for i in range(0, len(ids), CHUNK):
        yield from anki_request("notesInfo", notes=ids[i:i + CHUNK])["result"]


def get_sentence(note):
    raw = note["fields"]["Sentence"]["value"]
    return clean_anki_html(clean_cloze(raw))


def update_translation(note_id, translation):
    anki_request("updateNoteFields", note={"id": note_id, "fields": {"Translation": translation}})


def main():
    ids = get_notes_missing_translation()
    print(f"{len(ids)} notes missing translation")
    if not ids:
        return

    for note in fetch_notes(ids):
        note_id = note["noteId"]
        sentence = get_sentence(note)
        if not sentence:
            continue
        translation = translate_no_en(sentence)
        update_translation(note_id, translation)
        print(f"[{note_id}] {sentence!r} → {translation!r}")


if __name__ == "__main__":
    main()
