# DocVision AI — Local-First Document Q&A

DocVision AI is a **local-first** document Q&A application that follows the Mozilla.ai lightweight LLM workflow blueprint. It uses a **Find-Retrieve-Answer** pattern instead of traditional vector-database RAG — no embeddings, no vector DB, no cloud APIs.

Built with **PyMuPDF4LLM** for document extraction and **Ollama** for local inference using Qwen2.5:1.5b.

---

## Features

### Document Upload
- PDF, DOCX, TXT, CSV, Markdown, PNG, JPG, JPEG, BMP, TIFF
- OCR support via Tesseract for scanned images

### Find-Retrieve-Answer Workflow
- **Find**: LLM identifies the relevant document section from its heading
- **Retrieve**: Section content is loaded from disk
- **Answer**: LLM answers using only the retrieved section
- If the answer is incomplete, the LLM asks for more info and the next relevant section is checked

### Local LLM (no cloud APIs)
- Uses Ollama with Qwen2.5:1.5b (local inference, no API keys)
- Fully offline

### Persistent Storage
- SQLite database for chats, sources, and messages
- Section files stored on disk under `persist/`

### Development Tooling
- Pre-commit hooks for linting (ruff), formatting (ruff-format), type checking (pyrefly), security (bandit), and tests (pytest)

---

## System Architecture

```
User Uploads Documents
↓
PyMuPDF4LLM → Markdown → Split by Headings
↓
Section Files (persist/chat_X/sections/)
↓
User asks a question
↓
[FIND]  LLM selects the most relevant section heading
↓
[RETRIEVE]  Load that section's content from disk
↓
[ANSWER]  LLM answers based on the section content
↓
If answer is incomplete → go back to FIND (exclude current section)
```

---

## Project Structure

```
RAG-CHATBOT/
├── app.py                   # Streamlit UI
├── db.py                    # SQLite persistence (chats, sources, messages)
├── vector_functions.py      # Document extraction + section splitting + storage
├── local_llm.py             # Ollama Find-Retrieve-Answer workflow
├── pyproject.toml           # Tool configs (ruff, pyrefly, pytest)
├── .pre-commit-config.yaml  # Pre-commit hook definitions
├── requirements.txt         # Production dependencies
├── requirements-dev.txt     # Development dependencies
├── tests/
│   ├── __init__.py
│   ├── test_vector_functions.py
│   └── test_db.py
├── LICENSE                  # AGPLv3
├── .editorconfig            # Editor settings
├── .env.example             # Environment template
├── .gitlab-ci.yml           # CI pipeline
├── CONTRIBUTING.md          # Contribution guide
├── USER_MANUAL.md           # End-user documentation
├── AGENTS.md                # AI agent guide
├── CHANGELOG.md             # Release history
├── SECURITY.md              # Security policy
├── CODE_OF_CONDUCT.md       # Community standards
├── Dockerfile               # Container build
├── .dockerignore            # Docker build ignores
├── .env
├── persist/
│   └── chat_X/
│       └── sections/       # Individual .txt files per section
└── docvision.sqlite
```

---

## Technologies Used

- **PyMuPDF4LLM** — PDF to Markdown with heading structure
- **Ollama** — Local LLM server (Qwen2.5:1.5b)
- **RapidFuzz** — Fuzzy section-name matching
- **Streamlit** — UI framework
- **SQLite** — Chat/source/message persistence
- **Tesseract OCR** — Image text extraction
- **Pre-commit** — Linting (ruff), formatting (ruff-format), type checking (pyrefly), security (bandit), tests (pytest)

---

## Installation

### Prerequisites
- Python 3.10+
- [Ollama](https://ollama.ai) installed and running
- Tesseract OCR (optional, for image OCR)

### Setup
```bash
git clone <repository-url>
cd RAG-CHATBOT
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate      # Linux/Mac
pip install -r requirements.txt
```

### Pull the LLM model
```bash
ollama pull qwen2.5:1.5b
```

### Install dev dependencies (optional)
```bash
pip install -r requirements-dev.txt
pre-commit install
```

No API keys required.

---

## Run Application

```bash
streamlit run app.py
```

Opens at `http://localhost:8501` — make sure Ollama is running in the background.

---

## Usage

1. **Create a chat** session
2. **Upload PDFs or documents** — they are split into sections by headings
3. **Ask questions** — the LLM finds the right section and answers
4. **Review** which sections were consulted (shown below each answer)

---

## Future Improvements

- Support for more model sizes (3B, 7B)
- Source citations with page numbers
- Web page ingestion
- Multi-turn conversation memory improvements
- Chat export / PDF export

---

## Author

Sai Akshith Veerabathini

Built following the [Mozilla.ai Lightweight LLM Blueprint](https://blueprints.mozilla.ai/all-blueprints/query-structured-documents-using-a-lightweight-llm-workflow).
