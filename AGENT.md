# AGENT.md

## DocVision AI Agent

DocVision AI is an intelligent Retrieval-Augmented Generation (RAG) assistant designed to answer questions from uploaded documents and web sources.

### Responsibilities

The agent performs the following tasks:

1. Document Ingestion

   * Accepts PDF, DOCX, TXT, CSV, Markdown, and image files.
   * Extracts text using parsers and OCR.

2. Web Source Ingestion

   * Fetches public webpage content.
   * Extracts readable text for indexing.

3. Knowledge Indexing

   * Splits content into chunks.
   * Generates embeddings using Sentence Transformers.
   * Stores vectors using FAISS.

4. Information Retrieval

   * Finds relevant document chunks for a user query.
   * Retrieves top matching content from the vector store.

5. Response Generation

   * Uses Google Gemini to generate answers.
   * Grounds responses using retrieved context.

6. Chat Management

   * Maintains separate chat sessions.
   * Stores messages and sources in SQLite.

### Workflow

User Query
↓
Retrieve Relevant Chunks
↓
Build Prompt
↓
Gemini Generation
↓
Response Display

### Limitations

* Responses depend on indexed content.
* Web pages requiring authentication may not be accessible.
* OCR accuracy depends on image quality.
* Very large files may increase processing time.

### Future Enhancements

* Source citations
* Hybrid Search (BM25 + Vector Search)
* Export chat to PDF
* Multi-user authentication
* Cloud deployment
* Conversation memory improvements
