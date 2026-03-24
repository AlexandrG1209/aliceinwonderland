import requests
from pathlib import Path

BOOKS_DIR = Path("books")
BOOKS_DIR.mkdir(parents=True, exist_ok=True)

def get_book(book_id):
    path = BOOKS_DIR / f"{book_id}.txt"

    if path.exists():
        with open(path,"r", encoding="utf-8") as f:
            return f.read()
        
    url = f"https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt"

    print(f"Downloading book - {book_id}")

    response = requests.get(url)
    response.raise_for_status()

    text = response.text

    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

    return text