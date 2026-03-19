import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


def preprocess(text):
    text = text.lower()
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words("english"))

    tokens = [
        word for word in tokens
        if word.isalpha() and word not in stop_words
    ]

    return tokens

def clean_gutenberg(text):
    start = text.find("*** START")
    end = text.find("*** END")
    if start != -1:
        text = text[start:]
        text = text.split("\n", 1)[1]

    if end != -1:
        text = text[:end]
    return text