import sys
from loader import get_book
from preprocess import preprocess
from lexdiv import lex_div

book_id = sys.argv[1]

text = get_book(book_id)

tokens = preprocess(text)

result = lex_div(tokens)
print(result)