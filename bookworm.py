from loader import get_book

book_id = 743

text = get_book(book_id)

print(text[:500])