
from pathlib import Path

import pymupdf


def extract_pdf_text(pdf_path: str | Path) -> dict:
    """Extract text and page information from a PDF."""

    pdf_file = Path(pdf_path)

    # Check that the file exists.
    if not pdf_file.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_file}")

    # Check that the path points to a file.
    if not pdf_file.is_file():
        raise ValueError(f"Not a file: {pdf_file}")

    # Check the file extension.
    if pdf_file.suffix.lower() != ".pdf":
        raise ValueError("Only PDF files are supported.")

    try:
        with pymupdf.open(str(pdf_file)) as document:

            if document.needs_pass:
                raise ValueError("Password-protected PDFs are not supported.")

            pages = []

            for page_number, page in enumerate(document, start=1):
                page_text = page.get_text().strip()

                pages.append({
                    "page_number": page_number,
                    "text": page_text,
                    "has_text": bool(page_text)
                })

    except ValueError:
        raise
    except Exception as error:
        raise ValueError(
            f"Unable to read PDF '{pdf_file}': {error}"
        ) from error

    pages_without_text = [
        page["page_number"]
        for page in pages
        if not page["has_text"]
    ]

    full_text = "\n\n".join(
        page["text"] for page in pages if page["text"]
    )

    return {
        "file_name": pdf_file.name,
        "total_pages": len(pages),
        "total_characters": sum(len(page["text"]) for page in pages),
        "pages_without_text": pages_without_text,
        "pages": pages,
        "full_text": full_text
    }
