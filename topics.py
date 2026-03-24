from sklearn.feature_extraction.text import TfidfVectorizer


def build_topics_per_chapter(chapters_tokens, n_words=10):
    """
    Extract top words per chapter using TF-IDF.

    Parameters:
        chapters_tokens (list[list[str]]): tokenized chapters
        n_words (int): number of top words per chapter

    Returns:
        dict: {chapter_id: [word1, word2, ...]}
    """

    if not chapters_tokens:
        raise ValueError("Empty chapters_tokens")

    # Convert tokens back to text documents
    texts = [" ".join(tokens) for tokens in chapters_tokens]

    # Build TF-IDF matrix
    vectorizer = TfidfVectorizer(
        max_df=0.9,      # ignore very frequent words
        min_df=1,        # keep all words that appear at least once
        stop_words=None  # already handled in preprocess
    )

    X = vectorizer.fit_transform(texts)
    terms = vectorizer.get_feature_names_out()

    topics = {}

    # Extract top words for each chapter
    for i in range(X.shape[0]):
        row = X[i].toarray().flatten()

        # Sort words by importance
        indices = row.argsort()[::-1]

        # Take top N non-zero words
        words = []
        for idx in indices:
            if row[idx] <= 0:
                continue
            words.append(terms[idx])
            if len(words) == n_words:
                break

        topics[i + 1] = words

    return topics


def print_topics(topics):
    """
    Print topics in a readable format.
    """
    if not topics:
        print("No topics found")
        return

    for chapter_id, words in topics.items():
        print(f"Chapter {chapter_id}: {', '.join(words)}")