import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from vector_functions import (
    _sanitize_filename_part,
    extract_text_from_text,
    split_markdown_by_headings,
    text_to_sections,
)


def test_sanitize_filename_part_replaces_invalid_chars():
    result = _sanitize_filename_part("foo:bar*baz|qux?")
    assert ":" not in result
    assert "*" not in result
    assert "|" not in result
    assert "?" not in result


def test_sanitize_filename_part_truncates():
    result = _sanitize_filename_part("a" * 200)
    assert len(result) == 100


def test_extract_text_from_text_utf8():
    result = extract_text_from_text(b"hello world")
    assert result == "hello world"


def test_extract_text_from_text_empty():
    result = extract_text_from_text(b"")
    assert result == ""


def test_split_markdown_by_headings():
    md = "# Title\nsome content\n## Sub\ndetail"
    sections = split_markdown_by_headings(md)
    assert "Title" in sections
    assert "Sub" in sections
    assert "some content" in sections["Title"]
    assert "detail" in sections["Sub"]


def test_split_markdown_by_headings_no_headings():
    md = "just a paragraph\n\nanother line"
    sections = split_markdown_by_headings(md)
    assert "INTRO" in sections


def test_text_to_sections_non_pdf():
    sections = text_to_sections("hello", "notes.txt")
    assert sections == {"DOCUMENT": "hello"}


def test_text_to_sections_pdf():
    md = "# Intro\ncontent"
    sections = text_to_sections(md, "doc.pdf")
    assert "Intro" in sections
    assert "content" in sections["Intro"]


def test_text_to_sections_empty_text():
    assert text_to_sections("", "doc.pdf") is None
