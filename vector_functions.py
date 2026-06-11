import io
import os
import pickle
from pathlib import Path

import faiss
import numpy as np
import requests
from bs4 import BeautifulSoup
from docx import Document
from pdf2image import convert_from_bytes
from PIL import Image
from pypdf import PdfReader
import pytesseract

BASE_DIR = Path(__file__).resolve().parent
PERSIST_DIR = BASE_DIR / "persist"
PERSIST_DIR.mkdir(exist_ok=True)

_embedding_model = None

SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt",
    ".csv",
    ".md",
    ".png",
    ".jpg",
    ".jpeg",
    ".bmp",
    ".tiff",
}


def load_embedding_model():
    global _embedding_model
    if _embedding_model is None:
        from sentence_transformers import SentenceTransformer

        _embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    return _embedding_model


def extract_text_from_pdf(file_bytes, use_ocr=True, poppler_path=None):
    extracted_pages = []
    try:
        reader = PdfReader(io.BytesIO(file_bytes))
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                extracted_pages.append(page_text.strip())
    except Exception:
        pass

    document_text = "\n\n".join(extracted_pages).strip()
    if document_text or not use_ocr:
        return document_text

    try:
        images = (
            convert_from_bytes(file_bytes, poppler_path=poppler_path)
            if poppler_path
            else convert_from_bytes(file_bytes)
        )
        ocr_texts = []
        for image in images:
            ocr_text = pytesseract.image_to_string(image, lang="eng")
            if ocr_text.strip():
                ocr_texts.append(ocr_text.strip())
        return "\n\n".join(ocr_texts).strip()
    except Exception:
        return document_text


def extract_text_from_image(file_bytes):
    try:
        image = Image.open(io.BytesIO(file_bytes)).convert("RGB")
        return pytesseract.image_to_string(image, lang="eng").strip()
    except Exception:
        return ""


def extract_text_from_docx(file_bytes):
    try:
        document = Document(io.BytesIO(file_bytes))
        paragraphs = [p.text.strip() for p in document.paragraphs if p.text.strip()]
        return "\n\n".join(paragraphs).strip()
    except Exception:
        return ""


def extract_text_from_text(file_bytes):
    try:
        return file_bytes.decode("utf-8", errors="replace").strip()
    except Exception:
        return ""


def extract_text_from_url(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            return ""
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.get_text(separator="\n").strip()
    except Exception:
        return ""


def extract_text(file_bytes, filename, use_ocr=True, poppler_path=None):
    extension = Path(filename).suffix.lower()
    if extension == ".pdf":
        return extract_text_from_pdf(file_bytes, use_ocr=use_ocr, poppler_path=poppler_path)
    if extension in {".png", ".jpg", ".jpeg", ".bmp", ".tiff"}:
        return extract_text_from_image(file_bytes)
    if extension == ".docx":
        return extract_text_from_docx(file_bytes)
    if extension in {".txt", ".csv", ".md"}:
        return extract_text_from_text(file_bytes)
    return ""


def split_text(text, chunk_size=1000, overlap=200):
    text = text.replace("\r\n", "\n").strip()
    if not text:
        return []

    chunks = []
    start = 0
    while start < len(text):
        chunk = text[start : start + chunk_size].strip()
        if chunk:
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


def get_chat_dir(chat_id):
    chat_dir = PERSIST_DIR / f"chat_{chat_id}"
    chat_dir.mkdir(parents=True, exist_ok=True)
    return chat_dir


def get_index_file(chat_id):
    return get_chat_dir(chat_id) / "faiss_index.bin"


def get_chunks_file(chat_id):
    return get_chat_dir(chat_id) / "chunks.pkl"


def create_vector_store(chunks, chat_id):
    if not chunks:
        return False

    model = load_embedding_model()
    vectors = [model.encode(chunk, convert_to_numpy=True).astype(np.float32) for chunk in chunks]
    index = faiss.IndexFlatL2(vectors[0].shape[0])
    index.add(np.vstack(vectors))

    faiss.write_index(index, str(get_index_file(chat_id)))
    with open(get_chunks_file(chat_id), "wb") as file:
        pickle.dump(chunks, file)
    return True


def load_vector_store(chat_id):
    index_file = get_index_file(chat_id)
    chunks_file = get_chunks_file(chat_id)
    if not index_file.exists() or not chunks_file.exists():
        return None, []

    index = faiss.read_index(str(index_file))
    with open(chunks_file, "rb") as file:
        chunks = pickle.load(file)
    return index, chunks


def add_documents_to_chat(chat_id, documents):
    texts = []
    for document in documents:
        texts.extend(split_text(document))

    if not texts:
        return False

    index_file = get_index_file(chat_id)
    chunks_file = get_chunks_file(chat_id)
    model = load_embedding_model()
    new_vectors = [model.encode(chunk, convert_to_numpy=True).astype(np.float32) for chunk in texts]

    if index_file.exists() and chunks_file.exists():
        index, existing_chunks = load_vector_store(chat_id)
        if index is None:
            return create_vector_store(texts, chat_id)
        index.add(np.vstack(new_vectors))
        all_chunks = existing_chunks + texts
    else:
        index = faiss.IndexFlatL2(new_vectors[0].shape[0])
        index.add(np.vstack(new_vectors))
        all_chunks = texts

    faiss.write_index(index, str(index_file))
    with open(chunks_file, "wb") as file:
        pickle.dump(all_chunks, file)

    return True


def retrieve_chat(chat_id, query, top_k=8):
    index, chunks = load_vector_store(chat_id)
    if index is None or not chunks:
        return []

    model = load_embedding_model()
    query_vector = model.encode(query, convert_to_numpy=True).astype(np.float32)
    _, indices = index.search(np.array([query_vector], dtype=np.float32), top_k)
    return [chunks[i] for i in indices[0] if 0 <= i < len(chunks)]
