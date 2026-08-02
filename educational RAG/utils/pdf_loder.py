from pypdf import PdfReader
from pypdf.errors import PdfReadError


def load_pdf(pdf_path):
    pages = []

    try:
        reader = PdfReader(pdf_path)
    except (PdfReadError, FileNotFoundError, ValueError, TypeError):
        return pages

    for i, page in enumerate(reader.pages):
        text = page.extract_text()

        if text:
            pages.append(
                {
                    "page": i + 1,
                    "text": text
                }
            )

    return pages