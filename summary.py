import spacy

nlp = spacy.load("en_core_web_sm")

def summarise(text, n_sentences=4):
    """
    Summary of the given text using spacy by selecting the most important sentences of the text

    """
    # Converting the text into structured objects with a limited size to reduce the summary to beginning of book
    doc = nlp(text[:100000])

    # extracting the sentence from the text
    sentences = list(doc.sents)

    # Creating dictionary to store frequency at which each word appears
    word_freq = {}

    for token in doc:
        if token.is_alpha and not token.is_stop:
            word = token.text.lower()

            word_freq[word] = word_freq.get(word, 0) + 1
    

    sentence_score = {}

    for sentence in sentences:
        for token in sentence:
            word = token.text.lower()

            if word in word_freq:
                sentence_score[sentence] = sentence_score.get(sentence, 0) + word_freq[word]

        if sentence in sentence_score:
            sentence_score[sentence] /= len(sentence)
            
    top_sentences = sorted(sentence_score, key=sentence_score.get, reverse=True)[:n_sentences]

    summary = " ".join([sentence.text for sentence in top_sentences])

    return summary