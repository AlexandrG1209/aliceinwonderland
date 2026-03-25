from collections import Counter

def lex_div(tokens):
    # Total number of tokens
    tok = len(tokens)

    # Number of unique tokens
    typ = len(set(tokens))

    # Count how many times each word appears
    counts = Counter(tokens)

    # Hapax are words that appear only one time
    hap = sum(1 for w in counts if counts[w] == 1)

    # Type-token ratio
    ttr = round(typ / tok, 3) if tok else 0

    # Mean word length
    mwl = round(sum(len(w) for w in tokens) / tok, 3) if tok else 0

    # Mean word frequency
    mwf = round(tok / typ, 3) if typ else 0

    # Return all measures in one dictionary
    return {
        "tok": tok,
        "typ": typ,
        "hap": hap,
        "ttr": ttr,
        "mwl": mwl,
        "mwf": mwf
    }
