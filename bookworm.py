import argparse
import spacy
from loader import get_book
from preprocess import preprocess, clean_gutenberg
from lexdiv import lex_div
from entities import entities

nlp = spacy.load("en_core_web_sm")

parser = argparse.ArgumentParser(description="Book NLP tool")

parser.add_argument("book_id", type=int, help="Project Gutenberg book ID")

parser.add_argument("--lexdiv", action="store_true")
parser.add_argument("--entities", action="store_true")
parser.add_argument("--summarise", action="store_true")
parser.add_argument("--similar", action="store_true")

args = parser.parse_args()

# Loading book
text = get_book(args.book_id)
text = clean_gutenberg(text)


if args.lexdiv:
    print(lex_div(text))
if args.entities:
    import spacy

    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    print(entities(doc))

# Show topics for each chapter
if args.topics:
    topics = build_topics_per_chapter(chapters_tokens)
    print_topics(topics)

# These parts are not finished yet
if args.summarise:
    print("not done yet")
if args.similar:
    print("not done yet")

if not any([args.lexdiv, args.entities, args.summarise, args.similar]):
    print("invalid input, try again")
