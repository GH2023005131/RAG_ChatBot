# 📄 DocVision AI — Local-First Document Q&A

DocVision AI is a **local-first** document Q&A application that follows the Mozilla.ai lightweight LLM workflow blueprint. It uses a **Find-Retrieve-Answer** pattern instead of traditional vector-database RAG — no embeddings, no vector DB, no cloud APIs.

Built with **PyMuPDF4LLM** for document extraction and **Llama.cpp** (via `llama-cpp-python`) for local inference.

---

## 🚀 Features

### 📂 Document Upload
- PDF, DOCX, TXT, CSV, Markdown, PNG, JPG, JPEG, BMP, TIFF

### 🌐 Web Page Ingestion
- Add public webpage URLs — content is extracted and indexed

### 🔍 Find-Retrieve-Answer Workflow
- **Find**: LLM identifies the relevant document section from its heading
- **Retrieve**: Section content is loaded from disk
- **Answer**: LLM answers using only the retrieved section
- If the answer is incomplete, the LLM asks for more info and the next relevant section is checked

### 🤖 Local LLM (no cloud APIs)
- Uses `llama-cpp-python` with Qwen2.5-7B-Instruct GGUF model
- Fully offline — no API keys needed

### 💾 Persistent Storage
- SQLite database for chats, sources, and messages
- Section files stored on disk under `persist/`

### 🖼 OCR Support
- Tesseract OCR for scanned images and image-only PDFs

---

## 🏗 System Architecture

```
User Uploads Documents / URLs
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

## 📁 Project Structure

```
RAG-CHATBOT/
├── app.py               # Streamlit UI
├── db.py                # SQLite persistence (chats, sources, messages)
├── vector_functions.py  # Document extraction + section splitting + storage
├── local_llm.py         # Llama.cpp model loading + Find-Retrieve-Answer workflow
├── requirements.txt
├── .env
├── persist/
│   └── chat_X/
│       └── sections/    # Individual .txt files per section
└── docvision.sqlite
```

---

## ⚙️ Technologies Used

- **PyMuPDF4LLM** — PDF → Markdown with heading structure
- **Llama.cpp** (via `llama-cpp-python`) — Local GGUF model inference
- **Qwen2.5-7B-Instruct** (Q8_0 GGUF) — Default local model
- **RapidFuzz** — Fuzzy section-name matching
- **Streamlit** — UI framework
- **SQLite** — Chat/source/message persistence
- **Tesseract OCR** — Image text extraction

---

## 📦 Installation

### Prerequisites
- Python 3.10+
- 10 GB+ RAM (for 7B Q8 model)
- Optional: NVIDIA GPU with CUDA for GPU acceleration

### Setup
```bash
git clone <repository-url>
cd RAG-CHATBOT
python -m venv .venv
.venv\Scripts\activate     # Windows
# source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

No API keys required. The first run will download the Qwen2.5-7B-Instruct GGUF model (~7.6 GB) automatically to Hugging Face cache.

---

## ▶️ Run Application

```bash
streamlit run app.py
```

Opens at `http://localhost:8501`

---

## 📝 Usage

1. **Create a chat** session
2. **Upload PDFs or documents** — they are split into sections by headings
3. **Optionally add web URLs**
4. **Ask questions** — the LLM finds the right section and answers
5. **Review** which sections were consulted (shown below each answer)

---

## 🔮 Future Improvements

- Support for more model sizes (1.5B, 3B for lower-memory setups)
- Source citations with page numbers
- Multi-turn conversation memory improvements
- Chat export / PDF export

---

## 👨‍💻 Author

Sai Akshith Veerabathini

Built following the [Mozilla.ai Lightweight LLM Blueprint](https://blueprints.mozilla.ai/all-blueprints/query-structured-documents-using-a-lightweight-llm-workflow).
