from loader import get_book
import spacy

def entities(doc):
    # Using set() to not have duplicates in the lists
    locations = set()
    characters = set()
    for ent in doc.ents:
        if ent.label == "GPE":
            locations.append(ent.text)
        elif ent.label == "PERSON":
            characters.append(ent.text)

    entities = {"characters": characters, "locations": locations}
    return entities