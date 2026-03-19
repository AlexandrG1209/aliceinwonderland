import spacy
from loader import get_book
from preprocess import preprocess, clean_gutenberg
from lexdiv import lex_div
from entities import entities

nlp = spacy.load("en_core_web_sm")

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