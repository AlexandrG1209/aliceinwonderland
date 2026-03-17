from collections import Counter

def lex_div(tokens):

    tok = len(tokens)
    typ = len(set(tokens))
    counts = Counter(tokens)
    hap = sum(1 for w in counts if counts[w] == 1)
    ttr = typ/tok if tok else 0
    mwl = sum(len(w) for w in tokens) / tok if tok else 0
    mwf = tok / typ if typ else 0
    return {
        "tok": tok,
        "typ": typ,
        "hap": hap,
        "ttr": ttr,
        "mwl": mwl,
        "mwf": mwf
    }