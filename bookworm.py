import sys
from loader import get_book
from preprocess import preprocess
from lexdiv import lex_div

book_id = sys.argv[1]

text = get_book(book_id)

tokens = preprocess(text)

result = lex_div(tokens)
print(result)


print("--- Main Menu ---\n\n\n",
       "options:\n", 
       "1. quit"
       "2. Lexical diversity\n",
       "3. summary\n", 
       "4. Comparaison\n")

while user_opt != 1:
    user_opt = int(input("Enter an option >"))
    if user_opt == 1:
        break
    elif user_opt == 2:
        lex_div(tokens)