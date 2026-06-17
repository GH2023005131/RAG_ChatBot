---
name: document-ingestion
description: Use when working on document upload, text extraction, OCR, PDFs, DOCX, images, web URLs, supported file extensions, or Tesseract/Poppler behavior.
---

# Document Ingestion

Use this skill for adding or fixing source ingestion in DocVision AI.

## Project Context

- Supported extensions are declared in `SUPPORTED_EXTENSIONS` in `vector_functions.py`.
- PDF text extraction tries `pypdf` first and falls back to OCR through `pdf2image` and `pytesseract`.
- Image OCR uses `PIL.Image` and `pytesseract`.
- Web ingestion uses `requests` and `BeautifulSoup` in `extract_text_from_url()`.
- `POPPLER_PATH` is loaded from `.env` by `app.py` and passed into PDF extraction.

## Working Rules

- Return an empty string for failed extraction unless the caller is designed to handle exceptions.
- Keep file-type dispatch centralized in `extract_text()`.
- When adding a file type, update `SUPPORTED_EXTENSIONS`, extraction logic, and user-facing documentation if needed.
- Treat uploaded bytes as untrusted input; avoid writing raw uploads to disk unless required.
- For web URLs, keep timeouts and a browser-like user agent to avoid hanging the Streamlit app.

## Verification

- Test or inspect behavior for empty files, unsupported extensions, scanned PDFs, and malformed URLs.
- Confirm extracted text is stripped before indexing.
- Confirm failed extraction does not create empty FAISS indexes.
