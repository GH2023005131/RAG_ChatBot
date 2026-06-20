---
title: "RAG Workflow"
status: implemented
priority: high
---

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

## Implementation

- `vector_functions.py` — Text extraction and section management
- `local_llm.py` — Find-Retrieve-Answer orchestration via Ollama
- `db.py` — SQLite persistence for chats, sources, messages
- `app.py` — Streamlit UI with chat and document management

## Files

- `app.py`
- `db.py`
- `vector_functions.py`
- `local_llm.py`
