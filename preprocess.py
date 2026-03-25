import nltk
import re

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


# Tool used to reduce words to their base form
lemmatizer = WordNetLemmatizer()

# Load stop words if NLTK data is available
try:
    stop_words = set(stopwords.words("english"))
except LookupError:
    stop_words = set()


# This function cleans the text
def clean_text(text):
    # Remove numbers and punctuation
    text = re.sub(r"[^a-zA-Z\s]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# Main preprocessing function
def preprocess(text):
    # Lowercase the text first
    text = text.lower()

    # Clean the text before tokenization
    text = clean_text(text)

    # Tokenize the text, or use split if NLTK data is missing
    try:
        tokens = word_tokenize(text)
    except LookupError:
        tokens = text.split()

    # Keep only useful words and lemmatize them
    tokens = [
        _lemmatize(word)
        for word in tokens
        if word.isalpha() and word not in stop_words
    ]

    return tokens


def _lemmatize(word):
    # Lemmatize one word, or keep it if data is missing
    try:
        return lemmatizer.lemmatize(word)
    except LookupError:
        return word
    

def preprocess_chapters(chapter_texts):
    """
    This function preprocesses each chapter.

    Parameters:
        chapter_texts (list[str])

    Returns:
        list[list[str]]
    """
    # Apply preprocess() to each chapter
    return [preprocess(ch) for ch in chapter_texts]


def preprocess_full_text(chapter_texts):
    """
    This function joins all chapters and preprocesses them.

    It is useful for the full book analysis.
    """
    # Merge all chapters into one big text
    full_text = " ".join(chapter_texts)

    # Preprocess the complete text
    return preprocess(full_text)
