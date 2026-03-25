import argparse
from loader import get_book
from html_parser import extract_chapters
from preprocess import preprocess_chapters, preprocess_full_text
from lexdiv import lex_div
from entities import entities
from topics import build_topics_per_chapter, print_topics
from summary import summarise

# This parser reads the command line options
parser = argparse.ArgumentParser(description="Book NLP tool")

parser.add_argument("book_id", type=int, help="Project Gutenberg book ID")

parser.add_argument("--lexdiv", action="store_true")
parser.add_argument("--entities", action="store_true")
parser.add_argument("--topics", action="store_true")
parser.add_argument("--summarise", action="store_true")
parser.add_argument("--similar", action="store_true")

args = parser.parse_args()

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

# Show lexical diversity result
if args.lexdiv:
    print(lex_div(tokens))

# Show named entities like persons and places
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
    print(summarise(text))
if args.similar:
    print("not done yet")

# If the user gives no option, we print a message
if not any([args.lexdiv, args.entities, args.topics, args.summarise, args.similar]):
    print("invalid input, try again")


'''
print("--- Main Menu ---\n\n\n",
       "options:\n", 
       "1. quit\n"
       "2. Lexical diversity\n",
       "3. Named entities recognition\n"
       "4. summary\n", 
       "5. Comparaison\n")

user_opt = 0

while user_opt != 1:
    book_id = int(input("Enter book ID >"))
    user_opt = int(input("Enter an option >"))

    if user_opt == 1:
        break
    
    text = get_book(book_id)

    if user_opt == 2:
        tokens = preprocess(text)
        result =lex_div(tokens)
        print(result)
    
    elif user_opt == 3:
        doc = nlp(text)
        entities(doc)
''' 
