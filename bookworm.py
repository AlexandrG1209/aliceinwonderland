import argparse
import json

from loader import get_book
from html_parser import extract_chapters
from preprocess import preprocess_chapters, preprocess_full_text
from lexdiv import lex_div
from entities import entities
from topics import build_topics_per_chapter
from summary import summarise
from similarity import similar_books
from card import card

# This parser reads the command line options
parser = argparse.ArgumentParser(description="Book NLP tool")

parser.add_argument("book_id", type=int, help="Project Gutenberg book ID")

parser.add_argument("--lexdiv", action="store_true")
parser.add_argument("--entities", action="store_true")
parser.add_argument("--topics", action="store_true")
parser.add_argument("--summarize", "--summarise", dest="summarize", action="store_true")
parser.add_argument("--similar", action="store_true")
parser.add_argument("--card", action="store_true")

args = parser.parse_args()

# Shared book loading pipeline used by all CLI commands
# We load the book html from Gutenberg
html = get_book(args.book_id)
if not html:
    raise SystemExit("Could not load the book HTML.")

# We extract the chapters or big text parts
chapters = extract_chapters(html)
if not chapters:
    raise SystemExit("Could not extract any text from the book.")

# Full text for spaCy and tokens for lexical analysis
text = " ".join(chapters)
tokens = preprocess_full_text(chapters)
chapters_tokens = preprocess_chapters(chapters)

# Run only the command(s) requested by the user
# Show lexical diversity result
if args.lexdiv:
    print(lex_div(tokens))

# Show named entities like persons and places
if args.entities:
    import spacy

    nlp = spacy.load("en_core_web_sm")
    nlp.max_length = 2_000_000
    doc = nlp(text)
    print(entities(doc))

# Show topics for each chapter
if args.topics:
    topics = build_topics_per_chapter(chapters_tokens)
    print(topics)

# These parts are not finished yet
if args.summarize:
    print(summarise(text))
if args.similar:
    print(similar_books(args.book_id, target_text=" ".join(tokens)))

# Show all information on a card using json to give it formatting
if args.card:
    print(json.dumps(card(args.book_id, html, text, tokens, chapters_tokens), indent=2, ensure_ascii=False))

# If the user gives no option, we print a message
if not any([args.lexdiv, args.entities, args.topics, args.summarize, args.similar, args.card]):
    print("invalid input, try again")
