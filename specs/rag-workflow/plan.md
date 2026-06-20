# RAG Workflow — Implementation Plan

## Step 1: Document Extraction

Implement file parsers for each supported format in `vector_functions.py`.

## Step 2: Section Splitting

Split extracted markdown by headings using regex patterns.

## Step 3: Section Storage

Save each section as a `.txt` file under `persist/chat_{id}/sections/`.

## Step 4: Find-Retrieve-Answer Loop

Implement `find_retrieve_answer()` in `local_llm.py` using Ollama chat API.

## Step 5: Streamlit UI

Build chat management, document upload, and Q&A interface in `app.py`.

## Dependencies

- Ollama with qwen2.5:1.5b model
- PyMuPDF4LLM, python-docx, pytesseract, Pillow

## Risks

- OCR accuracy depends on image quality
- Large documents may have many sections
