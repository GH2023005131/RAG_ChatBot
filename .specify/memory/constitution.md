# Constitution

## Core Principles

1. **Local-First** — All processing runs locally. No data leaves the machine.
2. **Simplicity** — Prefer simple solutions over complex architectures. No vector DB, no embeddings.
3. **Find-Retrieve-Answer** — Follow the Mozilla.ai lightweight LLM workflow pattern.
4. **Testability** — Every module must have tests. All pre-commit hooks must pass before merging.

## Tech Stack

- Python 3.11+
- Streamlit (UI)
- Ollama (LLM inference)
- SQLite (persistence)
- PyMuPDF4LLM (PDF extraction)
- Tesseract OCR (image text)

## Pre-commit Standards

All code must pass:
- `ruff` — Linting
- `ruff-format` — Formatting
- `mypy` / `pyrefly` — Type checking
- `pyupgrade` — Modern syntax
- `bandit` / `detect-secrets` — Security
- `pytest` — Tests

## Branch Strategy

- `main` — Production-ready, protected
- Feature branches from `main`
- Conventional commits (`feat:`, `fix:`, `ci:`, etc.)
