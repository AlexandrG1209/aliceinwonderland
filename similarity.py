import json
from pathlib import Path

from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from html_parser import extract_chapters
from loader import get_book
from preprocess import preprocess_full_text


# Book list from the PDF subject
BOOK_TITLES = {
    11: "Alice's Adventures in Wonderland",
    12: "Through the Looking-Glass",
    16: "Peter Pan",
    55: "The Wonderful Wizard of Oz",
    113: "The Secret Garden",
    120: "Treasure Island",
    236: "The Jungle Book",
    108: "The Return of Sherlock Holmes",
    834: "The Memoirs of Sherlock Holmes",
    863: "The Mysterious Affair at Styles",
    1661: "The Adventures of Sherlock Holmes",
    61262: "Poirot Investigates",
    69087: "The Murder of Roger Ackroyd",
    70114: "The Big Four",
    35: "The Time Machine",
    36: "The War of the Worlds",
    84: "Frankenstein; Or, The Modern Prometheus",
    159: "The Island of Doctor Moreau",
    164: "Twenty Thousand Leagues under the Sea",
    345: "Dracula",
    68283: "The Call of Cthulhu",
}

# Save cleaned texts on disk to avoid doing the same work many times
CACHE_DIR = Path("cache")
CACHE_DIR.mkdir(parents=True, exist_ok=True)


def _cache_path(book_id):
    # One cache file for each book
    return CACHE_DIR / f"similarity_{book_id}.json"


def _load_cache(book_id):
    # Load cached data for one book
    path = _cache_path(book_id)
    if path.exists():
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    return {}


def _load_cached_text(book_id):
    # Load the cleaned text if it was already saved
    data = _load_cache(book_id)
    if "text" in data:
        return data["text"]
    return ""


def _save_cache(book_id, title="", text=""):
    # Save title and text in the same cache file
    path = _cache_path(book_id)
    with open(path, "w", encoding="utf-8") as file:
        json.dump({"id": book_id, "title": title, "text": text}, file)


def _build_book_text(book_id):
    # Use the cache first because preprocessing a full book takes time
    cached_text = _load_cached_text(book_id)
    if cached_text:
        # Stop here if the text is already ready
        return cached_text

    # Load the Gutenberg HTML book
    html = get_book(book_id)
    # Extract chapters or big sections from the HTML file
    chapters = extract_chapters(html)

    # Preprocess the full book and build one clean text string
    tokens = preprocess_full_text(chapters)
    text = " ".join(tokens)

    # Save the title and cleaned text for the next runs
    _save_cache(book_id, title=get_book_title(book_id), text=text)

    # Return the final cleaned text
    return text


def get_book_title(book_id):
    # Books from the PDF already have a known title
    if book_id in BOOK_TITLES:
        return BOOK_TITLES[book_id]

    # Use the cached title if it already exists
    data = _load_cache(book_id)
    if "title" in data and data["title"]:
        return data["title"]

    # For another book, load the HTML and read the title from the page
    html = get_book(book_id)
    soup = BeautifulSoup(html, "html.parser")

    # Read the title from the metadata in the head
    title_tag = soup.find("meta", attrs={"name": "dc.title"})
    if title_tag:
        title = title_tag.get("content", "").strip()
    else:
        # Fallback to the Gutenberg header line
        strong_title = soup.find("strong", string="Title")
        title_line = strong_title.parent.get_text(" ", strip=True)
        title = title_line.replace("Title", "", 1).replace(":", "", 1).strip()

    # Save the title even if the text is not built yet
    cached_text = data["text"] if "text" in data else ""
    _save_cache(book_id, title=title, text=cached_text)

    return title


def similar_books(target_id, target_text="", top_n=5):
    # Compare the target book with the fixed book list from the subject
    corpus_ids = list(BOOK_TITLES.keys())
    if target_id not in BOOK_TITLES:
        # Add the new target book if it is not in the PDF list
        corpus_ids.append(target_id)

    ids = []
    texts = []

    # Build the text corpus used for vectorization
    for book_id in corpus_ids:
        # Reuse the target text if we already have it in memory
        if book_id == target_id and target_text:
            text = target_text
        else:
            text = _build_book_text(book_id)

        # Keep ids and texts in the same order
        ids.append(book_id)
        texts.append(text)

    # Turn books into TF-IDF vectors and compare them with cosine similarity
    vectorizer = TfidfVectorizer(
        max_df=0.85,  # Ignore words that appear in too many books
        ngram_range=(1, 2),  # Use single words and pairs of words
        sublinear_tf=True,  # Reduce the effect of very frequent words
    )
    matrix = vectorizer.fit_transform(texts)
    similarities = cosine_similarity(matrix)

    # Find where the target book is in the corpus
    target_index = ids.index(target_id)
    # Get one score for each book in the corpus
    scores = list(enumerate(similarities[target_index]))
    # Sort from the most similar book to the least similar one
    scores.sort(key=lambda item: item[1], reverse=True)

    results = []
    for index, _score in scores:
        book_id = ids[index]
        if book_id == target_id:
            # Skip the same book
            continue

        # Return the closest book titles except the book itself
        results.append(get_book_title(book_id))
        if len(results) == top_n:
            # Stop when we have enough results
            break

    # Return the final list of similar books
    return results
