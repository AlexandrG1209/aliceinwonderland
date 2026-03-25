import requests
from pathlib import Path

# Folder where we save downloaded html books
BOOKS_DIR = Path("books_html")
BOOKS_DIR.mkdir(parents=True, exist_ok=True)


def get_book(book_id):
    # Local path for the html file
    path = BOOKS_DIR / f"{book_id}.html"

    # If the file already exists, load it from disk
    if path.exists():
        print("Loading from file")
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    # Gutenberg html url for the book
    url = f"https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}-images.html"

    print("Downloading:", url)

    try:
        # Send the request to download the html page
        response = requests.get(
            url,
            timeout=30,
            headers={"User-Agent": "bookworm/1.0"},
        )
        print("Status:", response.status_code)

        # Raise an error if the request failed
        response.raise_for_status()

    except Exception as e:
        print("ERROR:", e)
        return ""

    # Save the downloaded html text
    html = response.text
    print("Length:", len(html))

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)

    print("Saved!")

    # Return the html content
    return html
