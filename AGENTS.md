# AGENTS.md — DocVision AI Agent Guide

## Project Overview

DocVision AI is a Streamlit-based document Q&A application using Ollama for local LLM inference. It implements the Find-Retrieve-Answer pattern — no vector database or embeddings required.

## Tech Stack

- **Python 3.11** — Primary language
- **Streamlit** — UI framework
- **Ollama** — Local LLM server (Qwen2.5:1.5b)
- **SQLite** — Persistence layer
- **PyMuPDF4LLM** — PDF to Markdown extraction
- **Tesseract OCR** — Image text extraction

## Architecture

```
app.py                 — Streamlit UI and routing
db.py                  — SQLite chat/source/message persistence
vector_functions.py     — Document extraction, section splitting, file storage
local_llm.py           — Find-Retrieve-Answer workflow via Ollama
```

## Key Patterns

### Find-Retrieve-Answer Workflow

1. **Find**: LLM selects a relevant section heading from the list
2. **Retrieve**: Load that section's content from disk
3. **Answer**: LLM answers based on the section content
4. If incomplete → loop back, excluding the current section

### Section Storage

Documents are split into sections by headings. Each section is stored as a `.txt` file under `persist/chat_{id}/sections/`.

### Session Management

- Chat sessions are stored in SQLite
- Query parameter `chat_id` routes between home and chat views
- Sources are linked to chats via foreign keys

## Development

### Pre-commit Hooks

| Stage | Tool |
|-------|------|
| Linting | ruff |
| Formatting | ruff-format |
| Type checking | pyrefly |
| Tests | pytest |

### Running Tests

```bash
pytest -v
```

### Common Tasks

- **Add a new file format**: Add extension to `SUPPORTED_EXTENSIONS` in `vector_functions.py`, add extract function
- **Change LLM model**: Update model name in `local_llm.py` line 71
- **Add a database table**: Add schema in `db.py` `init_db()`, add CRUD functions
