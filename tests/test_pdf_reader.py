
import pymupdf
import pytest

from src.pdf_reader import extract_pdf_text


def create_pdf(file_path, page_texts):
    """Create a sample PDF for testing."""

    with pymupdf.open() as document:
        for text in page_texts:
            page = document.new_page()

            if text:
                page.insert_text((72, 72), text)

        document.save(str(file_path))


def test_extracts_text_from_multiple_pages(tmp_path):
    pdf_path = tmp_path / "sample.pdf"

    create_pdf(pdf_path, ["First page", "Second page"])

    result = extract_pdf_text(pdf_path)

    assert result["total_pages"] == 2
    assert result["pages"][0]["text"] == "First page"
    assert result["pages"][1]["text"] == "Second page"


def test_identifies_pages_without_text(tmp_path):
    pdf_path = tmp_path / "blank_page.pdf"

    create_pdf(pdf_path, ["Page one", "", "Page three"])

    result = extract_pdf_text(pdf_path)

    assert result["pages_without_text"] == [2]


def test_missing_pdf_raises_error(tmp_path):
    pdf_path = tmp_path / "missing.pdf"

    with pytest.raises(FileNotFoundError):
        extract_pdf_text(pdf_path)


def test_invalid_pdf_raises_error(tmp_path):
    pdf_path = tmp_path / "invalid.pdf"
    pdf_path.write_text("This is not a real PDF")

    with pytest.raises(ValueError):
        extract_pdf_text(pdf_path)
