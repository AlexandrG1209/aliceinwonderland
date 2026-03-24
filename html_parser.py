from bs4 import BeautifulSoup


def is_english(soup):
    """
    Check if the book is in English using the header.
    """
    header = soup.find("section", id="pg-header")

    if not header:
        return True

    lang_tag = header.find("strong", string="Language")

    if not lang_tag:
        return True

    text = lang_tag.parent.get_text().lower()

    return "english" in text


def remove_header_footer(soup):
    """
    Remove header and footer from the HTML.
    """
    header = soup.find("section", id="pg-header")
    if header:
        header.decompose()

    footer = soup.find("section", id="pg-footer")
    if footer:
        footer.decompose()


def extract_chapters(html):
    """
    Extract parts of the book (chapters or sections).
    """

    # parse HTML
    soup = BeautifulSoup(html, "html.parser")

    # check language
    if not is_english(soup):
        raise ValueError("Not English")

    # remove header and footer
    remove_header_footer(soup)

    # try to get chapters using div.chapter
    chapters = soup.find_all("div", class_="chapter")

    if chapters:
        texts = []
        for c in chapters:
            text = c.get_text(separator=" ").strip()
            if len(text) > 200:  # remove very small parts
                texts.append(text)
        return texts

    # fallback: split by headers (h2, h3)
    headers = soup.find_all(["h2", "h3"])

    texts = []

    for h in headers:
        section = []

        for sib in h.next_siblings:

            # stop if next header appears
            if getattr(sib, "name", None) in ["h2", "h3"]:
                break

            if hasattr(sib, "get_text"):
                section.append(sib.get_text())

        text = " ".join(section).strip()

        if len(text) > 200:
            texts.append(text)

    # last fallback: split whole text
    if not texts:
        full_text = soup.get_text(separator=" ")
        words = full_text.split()

        chunk_size = 2000
        texts = []

        for i in range(0, len(words), chunk_size):
            chunk = " ".join(words[i:i + chunk_size])
            texts.append(chunk)

    return texts