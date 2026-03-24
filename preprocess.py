import nltk
import re

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


# download 1 time
#import nltk
#nltk.download('punkt')
#nltk.download('punkt_tab')
#nltk.download('stopwords')
#nltk.download('wordnet')
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))


# cleaning 
def clean_text(text):

    # remove extra characters
    text = re.sub(r"[^a-zA-Z\s]", " ", text)

    # Remove multiple spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# main preprocess (tokenisation and lemmatization)
def preprocess(text):

    text = text.lower()

    text = clean_text(text)

    tokens = word_tokenize(text)

    tokens = [
        lemmatizer.lemmatize(word)
        for word in tokens
        if word.isalpha() and word not in stop_words
    ]

    return tokens
    

def preprocess_chapters(chapter_texts):
    """
    Apply preprocessing to a list of chapter texts.

    Parameters:
        chapter_texts (list[str])

    Returns:
        list[list[str]]
    """
    return [preprocess(ch) for ch in chapter_texts]


def preprocess_full_text(chapter_texts):
    """
    Combine all chapters into one text and preprocess it.

    Useful for:
        - summarization
        - similarity

    Returns:
        list[str]
    """
    full_text = " ".join(chapter_texts)
    return preprocess(full_text)