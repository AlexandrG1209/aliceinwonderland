import spacy

nlp = spacy.load("en_core_web_sm")
nlp.max_length = 2_000_000

def summarise(text, n_sentences=2):
    """
    Summary of the given text using spacy by selecting the most important sentences of the text

    """
    # Converting the text into structured objects with a limited size to reduce the summary to beginning of book
    doc = nlp(text)

    # extracting the sentence from the text
    sentences = list(doc.sents)

    # Creating dictionary to store frequency at which each word appears
    word_freq = {}
    
    # Loop through each character in in words
    for token in doc:

        # ignoring commun words
        if token.is_alpha and not token.is_stop:
            word = token.text.lower()

            # counting the number of times each word is used
            word_freq[word] = word_freq.get(word, 0) + 1
    

    sentence_score = {}

    for sentence in sentences:

        # loop through each word in sentences
        for token in sentence:
            word = token.text.lower()

            if word in word_freq:
                # add word importance to the sentence score
                sentence_score[sentence] = sentence_score.get(sentence, 0) + word_freq[word]
    # taking all the sentences and sorting them in a list of importance    
    top_sentences = sorted(sentence_score, key=sentence_score.get, reverse=True)[:n_sentences]

    # combining all the selected sentences into one chain of texte
    summary = " ".join([sentence.text for sentence in top_sentences])

    return summary
