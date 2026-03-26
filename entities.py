import re


BAD_ENTITIES = {
    "Said",
    "Chapter",
    "CHAPTER",
    "Miss",
    "Un",
    "Ma",
    "fig",
    "extras",
}


def _clean_entity_text(text):
    text = " ".join(text.split())
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _is_valid_entity(text):
    if len(text) < 3:
        return False
    if text.startswith("CHAPTER"):
        return False
    if text in BAD_ENTITIES:
        return False
    if any(char in text for char in ["\n", "\r", "(", ")", "[", "]", "{", "}"]):
        return False
    if text.lower() == text and " " not in text:
        return False
    return True


def entities(doc):
    # We use sets to avoid duplicates
    locations = set()
    characters = set()

    # We check each entity found by spaCy
    for ent in doc.ents:
        name = _clean_entity_text(ent.text)

        if not _is_valid_entity(name):
            continue

        if ent.label_ == "GPE":
            locations.add(name)
        elif ent.label_ == "PERSON":
            characters.add(name)

    # We return a simple text result
    return sorted(characters), sorted(locations)
