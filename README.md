# Bookworm

Bookworm is a simple NLP tool for Project Gutenberg books.  
It can analyze one book from the command line or from a small Streamlit dashboard.

## Features

- lexical diversity
- topic extraction
- named entities recognition
- book summarization
- book similarity
- book card

## Installation

Create a virtual environment and install the dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## CLI Usage

General form:

```bash
python3 bookworm.py <BOOK_ID> [OPTION]
```

Examples:

```bash
python3 bookworm.py 11 --lexdiv
python3 bookworm.py 11 --topics
python3 bookworm.py 11 --entities
python3 bookworm.py 11 --summarize
python3 bookworm.py 11 --similar
python3 bookworm.py 11 --card
```

Available options:

- `--lexdiv`
- `--topics`
- `--entities`
- `--summarize`
- `--similar`
- `--card`

## Dashboard

Run the frontend with:

```bash
streamlit run app.py
```

The dashboard lets you:

- choose a Gutenberg book ID
- select one or more analyses
- display the result in a simple interactive view

## Project Structure

- `bookworm.py` : CLI entry point
- `app.py` : Streamlit dashboard
- `loader.py` : HTML download and cache
- `html_parser.py` : chapter and metadata extraction
- `preprocess.py` : text preprocessing
- `lexdiv.py` : lexical diversity metrics
- `topics.py` : topic extraction
- `entities.py` : named entities extraction
- `summary.py` : extractive summary
- `similarity.py` : similarity with TF-IDF and cosine similarity
- `card.py` : book card aggregation

## Mermaid Diagrams

### Lexical Diversity

```mermaid
flowchart LR
    A[Book ID] --> B[Load HTML book]
    B --> C[Extract chapters]
    C --> D[Preprocess full text]
    D --> E[Count tokens types and hapax]
    E --> F[Compute TTR MWL and MWF]
    F --> G[Return lexdiv dictionary]
```

### Topic Modeling

```mermaid
flowchart LR
    A[Book ID] --> B[Load HTML book]
    B --> C[Extract chapters]
    C --> D[Preprocess each chapter]
    D --> E[Build TF-IDF vectors]
    E --> F[Select top words per chapter]
    F --> G[Return topics dictionary]
```

### Named Entities Recognition

```mermaid
flowchart LR
    A[Book ID] --> B[Load HTML book]
    B --> C[Extract full text]
    C --> D[Create spaCy document]
    D --> E[Detect named entities]
    E --> F[Keep people and places]
    F --> G[Return entities result]
```

### Summarization

```mermaid
flowchart LR
    A[Book ID] --> B[Load HTML book]
    B --> C[Extract full text]
    C --> D[Create spaCy document]
    D --> E[Compute word frequencies]
    E --> F[Score the sentences]
    F --> G[Select the best sentences]
    G --> H[Return summary]
```

### Similarity

```mermaid
flowchart LR
    A[Book ID] --> B[Load target book]
    B --> C[Load the PDF book collection]
    C --> D[Preprocess all books]
    D --> E[Build TF-IDF vectors]
    E --> F[Compute cosine similarity]
    F --> G[Return top 5 similar books]
```

### Book Card

```mermaid
flowchart LR
    A[Book ID] --> B[Load HTML book]
    B --> C[Run lexical diversity]
    C --> D[Run topics]
    D --> E[Run entities]
    E --> F[Run summary]
    F --> G[Run similarity]
    G --> H[Collect metadata]
    H --> I[Return book card]
```
