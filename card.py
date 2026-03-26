from preprocess import preprocess, clean_text  # text cleaning + tokenisation
from lexdiv import lex_div  # lexical diversity function
from entities import entities  # named entity recognition
from summary import summarise  # your summariser
# from similar import similar_books  # (add later when implemented)

import spacy

nlp = spacy.load("en_core_web_sm")  # load spaCy model


def card(book_id, text):

    cleaned_text = clean_text(text)

    tokens = preprocess(cleaned_text)

    lexdiv = lex_div(tokens)

    doc = nlp(cleaned_text)

    characters, locations = entities(doc)

    summary = summarise(cleaned_text)

    similar = ["Not implemented"]

    # Creating card and implementing variables from above
    card = {
        "info": {
            "id": str(book_id),
            "authors": "unknown",
            "bookshelves": "unknown"
        },

        "lexdiv": lexdiv,

        "topics": {},

        "entities": {
            "characters": characters,
            "locations": locations
        },

        "summary": summary,

        "similar": similar
    }

    return card
