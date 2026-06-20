# Contributing to DocVision AI

Thank you for your interest in contributing! All contributions are welcome.

## Development Setup

```bash
git clone <repository-url>
cd RAG-CHATBOT
python -m venv .venv
.venv\Scripts\activate    # Windows
# source .venv/bin/activate # Linux/Mac
pip install -r requirements-dev.txt
pre-commit install
```

## Pre-commit Hooks

All changes must pass pre-commit checks before committing:

- **ruff** — Linting
- **ruff-format** — Code formatting
- **pyrefly** — Type checking
- **pytest** — Unit tests

Run manually: `pre-commit run --all-files`

## Coding Standards

- Follow PEP 8 style (enforced by ruff)
- Add type annotations to all function signatures
- Write tests for new functionality in `tests/`
- Keep line length under 120 characters

## Pull Request Process

1. Create a feature branch from `main`
2. Make your changes
3. Run `pre-commit run --all-files` and ensure all pass
4. Submit a pull request with a clear description

## Reporting Issues

Open an issue with steps to reproduce, expected behavior, and actual behavior.
