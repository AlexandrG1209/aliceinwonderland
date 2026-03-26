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

    # Convert token lists into text strings
    texts = [" ".join(tokens) for tokens in chapters_tokens]

    # Create the TF-IDF vectorizer
    vectorizer = TfidfVectorizer(
        max_df=0.9,      # ignore very frequent words
        min_df=1,        # keep all words that appear at least once
        stop_words=None  # already handled in preprocess
    )

    # Build the TF-IDF matrix for all chapters
    X = vectorizer.fit_transform(texts)

    # Get the words from the vectorizer
    terms = vectorizer.get_feature_names_out()

    topics = {}

    # Process each chapter one by one
    for i in range(X.shape[0]):
        # Convert one chapter row into a simple array
        row = X[i].toarray().flatten()

        # Sort words from highest score to lowest score
        indices = row.argsort()[::-1]

        # Keep only the top important words
        words = []
        for idx in indices:
            if row[idx] <= 0:
                continue
            words.append(terms[idx])
            if len(words) == n_words:
                break

        # Save the result for this chapter
        topics[i + 1] = words

    return topics
