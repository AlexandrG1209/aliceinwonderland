from bs4 import BeautifulSoup


def _meta_content(soup, name):
    tag = soup.find("meta", attrs={"name": name})
    if tag:
        return tag.get("content", "").strip()
    return ""


def is_english(soup):
    """
    Check if the book is in English using the header.
    """
    # We try to find the Gutenberg header section
    header = soup.find("section", id="pg-header")

    # If there is no header, we accept the book
    if not header:
        return True

    # We look for the language label in the header
    lang_tag = header.find("strong", string="Language")

    # If we do not find the label, we accept the book
    if not lang_tag:
        return True

    # We read the full text around the language label
    text = lang_tag.parent.get_text().lower()

    # We return True only if the word english is present
    return "english" in text


def remove_header_footer(soup):
    """
    Remove header and footer from the HTML.
    """
    # Remove the Gutenberg header if it exists
    header = soup.find("section", id="pg-header")
    if header:
        header.decompose()

    # Remove the Gutenberg footer if it exists
    footer = soup.find("section", id="pg-footer")
    if footer:
        footer.decompose()


def extract_book_info(html, book_id):
    """
    Extract basic metadata from the Gutenberg header
    """
    soup = BeautifulSoup(html, "html.parser")
    header = soup.find("section", id="pg-header")

    # Start with fallback values in case some metadata is missing
    info = {
        "id": str(book_id),
        "authors": "unknown",
        "bookshelves": "unknown",
    }

    if not header:
        return info

    # Metadata in the head is usually cleaner than the visible header text
    author = _meta_content(soup, "dc.creator")
    if author:
        info["authors"] = author

    subjects = [
        tag.get("content", "").strip()
        for tag in soup.find_all("meta", attrs={"name": "dc.subject"})
        if tag.get("content", "").strip()
    ]
    if subjects:
        info["bookshelves"] = "; ".join(subjects)

    return info


def extract_chapters(html):
    """
    Extract parts of the book (chapters or sections).
    """

    # We parse the html content
    soup = BeautifulSoup(html, "html.parser")

    # We check if the book is in English
    if not is_english(soup):
        raise ValueError("Not English")

    # We remove the Gutenberg header and footer
    remove_header_footer(soup)

    # First we try to find chapters with div.chapter
    chapters = soup.find_all("div", class_="chapter")

    if chapters:
        texts = []
        for c in chapters:
            # Get clean text from each chapter block
            text = c.get_text(separator=" ").strip()
            # We ignore very small parts
            if len(text) > 200:
                texts.append(text)
        return texts

    # If no chapter div exists, we try with h2 and h3 titles
    headers = soup.find_all(["h2", "h3"])

    texts = []

    for h in headers:
        # This list stores the text of one section
        section = []

        for sib in h.next_siblings:

            # Stop when the next title starts
            if getattr(sib, "name", None) in ["h2", "h3"]:
                break

            # Keep only elements that can return text
            if hasattr(sib, "get_text"):
                section.append(sib.get_text())

        # Join all parts of the section into one string
        text = " ".join(section).strip()

        # Keep only sections with enough text
        if len(text) > 200:
            texts.append(text)

    # Last fallback: split the whole book into big chunks
    if not texts:
        full_text = soup.get_text(separator=" ")
        words = full_text.split()

        chunk_size = 2000
        texts = []

        for i in range(0, len(words), chunk_size):
            # Make one chunk from 2000 words
            chunk = " ".join(words[i:i + chunk_size])
            texts.append(chunk)

    # Return all extracted parts
    return texts
