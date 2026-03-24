from collections import Counter


def topics_per_chapter(chapters_tokens):
    """
    For each chapter:
    - count word frequencies
    - take top 10 words
    """

    result = {}

    for i, tokens in enumerate(chapters_tokens):

        if not tokens:
            continue

        counts = Counter(tokens)

        # get 10 most common words
        most_common = counts.most_common(10)

        # keep only words
        words = [word for word, freq in most_common]

        result[i + 1] = words

    return result