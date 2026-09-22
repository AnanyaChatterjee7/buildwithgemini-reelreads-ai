# My agent: ReelReads AI

One-liner: An AI Book Concierge that helps readers discover personalized books, track reading lists and progress, explore grounded literary analysis, and generate original AI cover art.

## Tool Coverage

- **Memory**: Remembers reading preferences, favorite genres, authors, and reading speed across sessions via **Vertex AI Memory Bank**.
- **Tools**:
  - `search_books_openlibrary`: Live book search & metadata retrieval via **Open Library API**.
  - `firestore_reading_list`: Manage reading lists ("Want to Read", "Currently Reading", "Read") & reading progress in **Cloud Firestore**.
  - `rag_literary_qa`: Grounded literary Q&A, plot analyses, and character insights using **Vertex AI RAG Engine**.
  - `generate_cover_art`: Generates original AI book cover art using `gemini-3.1-flash-lite-image` / Nano Banana 2 Lite.
- **Catalog/UI**: **A2UI cards and carousels** for visual book rows, personalized recommendation carousels, reading shelf cards, and progress meters.
- **Image Gen**: Original AI cover art generation for custom editions or user-imagined concepts.
- **Sandbox/Compute**: Calculates reading velocity, estimated completion dates, and reading streak metrics.

## Core Rails & Stretch Features
- **Core rails**: ADK agent structure, sessions/memory, function tools, evaluation dataset, Cloud Run deployment.
- **Stretch menu**: A2UI rich card rendering, Firestore persistent storage, Vertex AI RAG grounded knowledge, AI image generation, custom mobile-friendly FastAPI frontend.

## First Evaluation Question
"Recommend 3 sci-fi space opera novels similar to *Hyperion*, add *Dune* to my 'Currently Reading' list at 45% progress, and generate a cinematic cover art for a custom edition."
