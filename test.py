from loader import get_book_html
from html_parser import extract_chapters
from preprocess import preprocess
from topics import build_lda, print_topics
from lexdiv import lex_div


def main():
    print("START")

    # 1. Load book
    html = get_book_html(11)
    print("HTML loaded")

    # 2. Extract chapters
    chapters = extract_chapters(html)
    print("Chapters:", len(chapters))

    if not chapters:
        print("ERROR: No chapters found")
        return

    # 3. Preprocess all chapters
    chapters_tokens = [preprocess(ch) for ch in chapters]
    print("Preprocess done")

    # check first tokens
    print("Sample tokens:", chapters_tokens[0][:20])

    # 4. Lexical diversity (on first chapter)
    stats = lex_div(chapters_tokens[0])
    print("\nLEXICAL DIVERSITY:")
    for k, v in stats.items():
        print(k, ":", v)

    # 5. LDA
    lda = build_lda(chapters_tokens, num_topics=3)

    print("\nTOPICS:")
    print_topics(lda)


if __name__ == "__main__":
    main()