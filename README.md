```md
## Lexical Diversity Diagram

```mermaid
flowchart LR
    A[Book ID] --> B[Load HTML book]
    B --> C[Extract chapters]
    C --> D[Preprocess full text]
    D --> E[Count tokens types and hapax]
    E --> F[Compute TTR MWL and MWF]
    F --> G[Return lexdiv dictionary]