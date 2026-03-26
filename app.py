import streamlit as st
import spacy

from entities import entities
from html_parser import extract_book_info, extract_chapters
from lexdiv import lex_div
from loader import get_book
from preprocess import preprocess_chapters, preprocess_full_text
from similarity import get_book_title, similar_books
from summary import summarise
from topics import build_topics_per_chapter


st.set_page_config(
    page_title="Bookworm Dashboard",
    layout="wide",
)


@st.cache_resource
def load_nlp():
    # Load spaCy once and reuse it across Streamlit reruns
    nlp = spacy.load("en_core_web_sm")
    nlp.max_length = 2_000_000
    return nlp


def load_book_data(book_id):
    # Reuse the same loading pipeline as the CLI
    html = get_book(book_id)
    if not html:
        raise ValueError("Could not load the book HTML")

    chapters = extract_chapters(html)
    if not chapters:
        raise ValueError("Could not extract any text from the book")

    text = " ".join(chapters)
    tokens = preprocess_full_text(chapters)
    chapters_tokens = preprocess_chapters(chapters)

    return html, chapters, text, tokens, chapters_tokens


st.title("Bookworm Dashboard")
st.write("A simple interface to explore lexical diversity, topics, entities, summary and similarity")

with st.sidebar:
    st.header("Controls")
    book_id = st.number_input("Project Gutenberg book ID", min_value=1, value=11, step=1)
    selected_tasks = st.multiselect(
        "Choose analyses",
        ["Lexical Diversity", "Topics", "Entities", "Summary", "Similarity"],
        default=["Lexical Diversity", "Topics", "Entities", "Summary", "Similarity"],
    )
    run_analysis = st.button("Analyze Book", use_container_width=True)


if run_analysis:
    try:
        # Load everything once so each analysis can reuse the same data
        html, chapters, text, tokens, chapters_tokens = load_book_data(int(book_id))
        title = get_book_title(int(book_id))
        book_info = extract_book_info(html, int(book_id))
    except Exception as error:
        st.error(str(error))
    else:
        st.subheader(title)
        col1, col2, col3 = st.columns(3)
        col1.metric("Book ID", int(book_id))
        col2.metric("Sections", len(chapters))
        col3.metric("Tokens", len(tokens))
        st.write(f"**Author:** {book_info['authors']}")
        st.write(f"**Bookshelves:** {book_info['bookshelves']}")

        if "Lexical Diversity" in selected_tasks:
            st.subheader("Lexical Diversity")
            lexdiv_result = lex_div(tokens)
            # Show the six main lexical metrics in a compact way
            metric_col1, metric_col2, metric_col3 = st.columns(3)
            metric_col1.metric("Tokens", lexdiv_result["tok"])
            metric_col2.metric("Types", lexdiv_result["typ"])
            metric_col3.metric("Hapax", lexdiv_result["hap"])
            metric_col4, metric_col5, metric_col6 = st.columns(3)
            metric_col4.metric("TTR", lexdiv_result["ttr"])
            metric_col5.metric("Mean Word Length", lexdiv_result["mwl"])
            metric_col6.metric("Mean Word Frequency", lexdiv_result["mwf"])

        if "Topics" in selected_tasks:
            st.subheader("Topics")
            topics = build_topics_per_chapter(chapters_tokens)
            # Show one expandable block per section of the book
            for chapter_id, words in topics.items():
                with st.expander(f"Section {chapter_id}"):
                    st.write(", ".join(words))

        if "Entities" in selected_tasks:
            st.subheader("Named Entities")
            nlp = load_nlp()
            doc = nlp(text)
            characters, locations = entities(doc)
            # Separate characters and locations to make the result easier to read
            entity_col1, entity_col2 = st.columns(2)
            with entity_col1:
                st.markdown("**Characters**")
                for name in characters:
                    st.write(f"- {name}")
            with entity_col2:
                st.markdown("**Locations**")
                for name in locations:
                    st.write(f"- {name}")

        if "Summary" in selected_tasks:
            st.subheader("Summary")
            st.write(summarise(text))

        if "Similarity" in selected_tasks:
            st.subheader("Similar Books")
            similar = similar_books(int(book_id), target_text=" ".join(tokens))
            # Keep the output simple with one title per line
            for title in similar:
                st.write(f"- {title}")

else:
    st.info("Choose a book ID in the sidebar and click Analyze Book")
