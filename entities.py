def entities(doc):
    # We use sets to avoid duplicates
    locations = set()
    characters = set()

    # We check each entity found by spaCy
    for ent in doc.ents:
        if ent.label_ == "GPE":
            locations.add(ent.text)
        elif ent.label_ == "PERSON":
            characters.add(ent.text)

    # We return a simple text result
    return sorted(characters), sorted (locations)
