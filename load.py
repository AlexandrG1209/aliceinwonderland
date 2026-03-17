import requests
import os


def download_book(book_id: int, save_dir: str = "data") -> str:
    """
    Download a book from Project Gutenberg and save it locally.

    Args:
        book_id (int): Gutenberg book ID
        save_dir (str): Directory to save the book

    Returns:
        str: Path to saved file
    """

    # URL Gutenberg (format standard)
    url = f"https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt"

    # Créer dossier si existe pas
    os.makedirs(save_dir, exist_ok=True)

    file_path = os.path.join(save_dir, f"{book_id}.txt")

    try:
        print(f"Downloading book {book_id}...")

        response = requests.get(url)

        if response.status_code != 200:
            raise Exception(f"Failed to download (status {response.status_code})")

        text = response.text

        # Nettoyage basique (header/footer Gutenberg)
        start_marker = "*** START OF"
        end_marker = "*** END OF"

        start = text.find(start_marker)
        end = text.find(end_marker)

        if start != -1 and end != -1:
            text = text[start:end]

        # Sauvegarde
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text)

        print(f"Saved to {file_path}")
        return file_path

    except Exception as e:
        print(f"Error: {e}")
        return ""