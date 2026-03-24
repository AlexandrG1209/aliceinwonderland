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
    doc = nlp(text)
    print(entities(doc))
if args.summarise:
    print("not done yet")
if args.similar:
    print("not done yet")

if not any([args.lexdiv, args.entities, args.summarise, args.similar]):
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