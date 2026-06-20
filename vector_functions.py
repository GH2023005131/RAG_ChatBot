import io
import re
import tempfile
from collections import defaultdict
from pathlib import Path

import pymupdf4llm
import pytesseract
from docx import Document
from PIL import Image

BASE_DIR = Path(__file__).resolve().parent
PERSIST_DIR = BASE_DIR / "persist"

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


def extract_text_from_pdf(file_bytes, poppler_path=None):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(file_bytes)
            pdf_path = tmp.name
        md_text = pymupdf4llm.to_markdown(pdf_path)
        Path(pdf_path).unlink(missing_ok=True)
        return md_text
    except Exception as e:
        print("PDF extraction error:", e)
        return ""


def extract_text_from_image(file_bytes):
    try:
        image = Image.open(io.BytesIO(file_bytes)).convert("RGB")
        result = pytesseract.image_to_string(image, lang="eng")
        return result.strip() if isinstance(result, str) else str(result)
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


def extract_text(file_bytes, filename, poppler_path=None):
    extension = Path(filename).suffix.lower()
    if extension == ".pdf":
        return extract_text_from_pdf(file_bytes, poppler_path=poppler_path)
    if extension in {".png", ".jpg", ".jpeg", ".bmp", ".tiff"}:
        return extract_text_from_image(file_bytes)
    if extension == ".docx":
        return extract_text_from_docx(file_bytes)
    if extension in {".txt", ".csv", ".md"}:
        return extract_text_from_text(file_bytes)
    return ""


def split_markdown_by_headings(markdown_text):
    heading_patterns = [
        r"^#\s+(.+)$",
        r"^##\s+(.+)$",
        r"^###\s+(.+)$",
        r"^####\s+(.+)$",
        r"^\*\*[\d\.]+\.\*\*\s*\*\*(.+)\*\*$",
    ]
    sections: dict = defaultdict(str)
    heading_text = "INTRO"
    for line in markdown_text.splitlines():
        line = line.strip()
        if not line:
            continue
        for pattern in heading_patterns:
            match = re.match(pattern, line)
            if match:
                heading_text = match.group(1)[:100]
                break
        sections[heading_text] += f"{line}\n"
    return dict(sections)


def text_to_sections(text, filename):
    if not text:
        return None
    sections = split_markdown_by_headings(text) if filename.lower().endswith(".pdf") else {"DOCUMENT": text}
    return sections


def get_sections_dir(chat_id):
    d = PERSIST_DIR / f"chat_{chat_id}" / "sections"
    d.mkdir(parents=True, exist_ok=True)
    return d


_INVALID_CHARS = set('\\/:*?"<>|')


def _sanitize_filename_part(text):
    return "".join("_" if c in _INVALID_CHARS else c for c in text)[:100]


def save_sections(chat_id, sections, source_name=""):
    sections_dir = get_sections_dir(chat_id)
    prefix = ""
    if source_name:
        prefix = f"{_sanitize_filename_part(source_name)}_"
    names = []
    for name, content in sections.items():
        safe = _sanitize_filename_part(name)
        safe = f"{prefix}{safe}"
        (sections_dir / f"{safe}.txt").write_text(content, encoding="utf-8")
        names.append(safe)
    return names


def get_section_names(chat_id):
    sections_dir = get_sections_dir(chat_id)
    return sorted([f.stem for f in sections_dir.glob("*.txt")])


def get_section_content(chat_id, section_name):
    sections_dir = get_sections_dir(chat_id)
    f = sections_dir / f"{section_name}.txt"
    return f.read_text(encoding="utf-8") if f.exists() else ""


def clear_sections(chat_id):
    sections_dir = get_sections_dir(chat_id)
    if sections_dir.exists():
        for f in sections_dir.glob("*"):
            f.unlink()
