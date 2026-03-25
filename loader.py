import requests
from pathlib import Path

BOOKS_DIR = Path("books_html")
BOOKS_DIR.mkdir(parents=True, exist_ok=True)


def get_book(book_id):
    path = BOOKS_DIR / f"{book_id}.html"

    if path.exists():
        print("Loading from file")
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    url = f"https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}-images.html"

    print("Downloading:", url)

    try:
        response = requests.get(url)
        print("Status:", response.status_code)

        response.raise_for_status()

    except Exception as e:
        print("ERROR:", e)
        return ""

    html = response.text
    print("Length:", len(html))

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)

    print("Saved!")

    return html
