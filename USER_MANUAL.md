# DocVision AI — User Manual

## Overview

DocVision AI is a local-first document Q&A application. Upload documents and ask questions — the LLM finds relevant sections and answers using only your documents.

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.ai) installed and running
- Tesseract OCR (optional, for image OCR)

## Getting Started

### 1. Start Ollama

```bash
ollama pull qwen2.5:1.5b
ollama serve
```

### 2. Launch the App

```bash
streamlit run app.py
```

Open `http://localhost:8501`.

## Using the Application

### Creating a Chat

1. On the home page, enter a chat title
2. Click **Create chat**

### Uploading Documents

1. Inside a chat, use the sidebar file uploader
2. Select one or more files (PDF, DOCX, TXT, CSV, MD, PNG, JPG, JPEG, BMP, TIFF)
3. Click **Add documents**
4. The app extracts text, splits into sections, and indexes them

### Asking Questions

1. Type your question in the chat input at the bottom
2. The LLM finds the relevant section and answers
3. Consulted sections are shown below each answer

### Managing Sources

- View uploaded sources in the sidebar
- Delete individual sources with the ❌ button
- Sources are automatically re-indexed when deleted

### Managing Chats

- Switch between chats from the home page
- Delete chats using the **Delete** button

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Ollama connection error | Ensure `ollama serve` is running |
| No documents found | Upload documents before asking questions |
| OCR not working | Install Tesseract and set POPPLER_PATH in `.env` |
| Slow answers | The 1.5B model runs on CPU; patience required |

## FAQ

**Q: Are my documents sent to the cloud?**  
A: No. Everything runs locally — no data leaves your machine.

**Q: What file types are supported?**  
A: PDF, DOCX, TXT, CSV, MD, PNG, JPG, JPEG, BMP, TIFF.

**Q: Can I use a different model?**  
A: Change the model name in `local_llm.py` (line 71) from `qwen2.5:1.5b` to any Ollama model.
