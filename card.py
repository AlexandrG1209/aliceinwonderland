from entities import entities
from html_parser import extract_book_info
from lexdiv import lex_div
from similarity import similar_books
from summary import summarise
from topics import build_topics_per_chapter

import spacy

# The card also uses spaCy for named entities
nlp = spacy.load("en_core_web_sm")
nlp.max_length = 2_000_000


def card(book_id, html, text, tokens, chapters_tokens):
    # Reuse the outputs of the existing modules to build one final object
    lexdiv = lex_div(tokens)

    doc = nlp(text)

    characters, locations = entities(doc)

    summary = " ".join(summarise(text).split())
    topics = build_topics_per_chapter(chapters_tokens)
    similar = similar_books(book_id, target_text=" ".join(tokens))

    # Gather all results in the structure expected by the project subject
    card = {
        "info": extract_book_info(html, book_id),

        "lexdiv": lexdiv,

        "topics": topics,

        "entities": {
            "characters": characters,
            "locations": locations
        },

        "summary": summary,

        "similar": similar
    }

    return card
