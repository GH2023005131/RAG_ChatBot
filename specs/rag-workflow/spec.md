# RAG Workflow

## Summary

Implement the Find-Retrieve-Answer document Q&A workflow using a local LLM.

## Requirements

- Accept document uploads (PDF, DOCX, TXT, CSV, MD, images)
- Extract text and split into sections by headings
- Store sections as individual files on disk
- On user question, LLM selects the relevant section heading
- Load section content and LLM answers based on it
- If answer incomplete, loop to next relevant section
- Support OCR for scanned images

## Technical Approach

Use Ollama with Qwen2.5:1.5b for local inference. Documents are extracted via PyMuPDF4LLM (PDF) and Tesseract (images), split by markdown headings, and stored as `.txt` files. The Find-Retrieve-Answer loop selects sections, loads content, and answers iteratively.

## Acceptance Criteria

- [x] PDF, DOCX, TXT, CSV, MD, and image files can be uploaded
- [x] Text is extracted and split into sections by headings
- [x] LLM selects the correct section for a given question
- [x] LLM answers based only on the retrieved section
- [x] If answer is incomplete, next section is checked
- [x] OCR works for scanned images

## Files

- `vector_functions.py`
- `local_llm.py`
- `db.py`
- `app.py`
