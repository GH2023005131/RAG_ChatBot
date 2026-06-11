# 📄 DocVision AI

DocVision AI is a Retrieval-Augmented Generation (RAG) application that enables users to upload documents, add web sources, and ask intelligent questions based on the indexed content.

The system combines document processing, OCR, vector search, and Google's Gemini model to provide context-aware answers from user-provided knowledge sources.

---

## 🚀 Features

### 📂 Document Upload

Supports:

* PDF
* DOCX
* TXT
* CSV
* Markdown
* PNG
* JPG
* JPEG
* BMP
* TIFF

### 🌐 Web Page Ingestion

* Add public webpage URLs
* Extract webpage content automatically
* Index content for question answering

### 🔍 Retrieval-Augmented Generation (RAG)

* Text chunking
* Semantic embeddings
* FAISS vector search
* Context retrieval

### 🤖 AI-Powered Answers

* Google Gemini 2.5 Flash
* Context-aware responses
* Multi-turn conversation support

### 💾 Persistent Storage

* SQLite database
* Persistent chat sessions
* Stored source documents
* Saved chat history

### 🖼 OCR Support

* Extract text from scanned images
* Tesseract OCR integration
* PDF image processing

---

# 🏗 System Architecture

User Uploads Documents / URLs
↓
Text Extraction
↓
Chunking
↓
Embeddings Generation
↓
FAISS Vector Store
↓
Context Retrieval
↓
Gemini LLM
↓
Answer Generation

---

# 📁 Project Structure

```text
RAG-CHATBOT/
│
├── AGENT.md
├── SKILLS.md
├── README.md
├── app.py
├── db.py
├── vector_functions.py
├── requirements.txt
├── .gitignore
│
├── persist/
│   └── chat_x/
│
└── docvision.sqlite
```

---

# ⚙️ Technologies Used

## Frontend

* Streamlit

## Backend

* Python

## AI & NLP

* Google Gemini API
* Sentence Transformers
* Retrieval-Augmented Generation (RAG)

## Vector Database

* FAISS

## OCR

* Tesseract OCR
* PDF2Image
* Pillow

## Database

* SQLite

## Web Processing

* BeautifulSoup
* Requests

---

# 📦 Installation

## Clone Repository

```bash
git clone <repository-url>
cd RAG-CHATBOT
```

## Create Virtual Environment

```bash
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

### Linux / Mac

```bash
source .venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Setup

Create a `.env` file:

```env
GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
```

Optional:

```env
POPPLER_PATH=C:\poppler\Library\bin
```

---

# ▶️ Run Application

```bash
streamlit run app.py
```

Application opens at:

```text
http://localhost:8501
```

---

# 📝 Usage

### Step 1

Create a chat session.

### Step 2

Upload one or more documents.

### Step 3

Optionally add webpage URLs.

### Step 4

Ask questions based on indexed content.

### Step 5

Receive context-aware AI-generated answers.

---

# 📸 Screenshots

## Dashboard

(Add Screenshot Here)

## Upload Documents

(Add Screenshot Here)

## Question Answering

(Add Screenshot Here)

---

# 🎯 Key Skills Demonstrated

* Retrieval-Augmented Generation (RAG)
* Semantic Search
* Vector Databases
* OCR Processing
* Prompt Engineering
* Streamlit Development
* SQLite Database Design
* Web Content Extraction
* AI Application Development

---

# 🔮 Future Improvements

* Source Citations
* PDF Export
* Chat Export
* Multi-user Authentication
* Hybrid Search (BM25 + Vector Search)
* Cloud Deployment
* Conversation Memory Enhancements

---

# 👨‍💻 Author

Sai Akshith Veerabathini

Built as an AI-powered document intelligence assistant using Streamlit, FAISS, OCR, and Google Gemini.
