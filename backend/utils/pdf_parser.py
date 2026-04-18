import os
import re

import pdfplumber
from docx import Document


def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from a PDF file using pdfplumber."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"PDF file not found: {file_path}")

    try:
        with pdfplumber.open(file_path) as pdf:
            if len(pdf.pages) == 0:
                raise ValueError(f"PDF has no pages: {file_path}")

            pages_text = []
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    pages_text.append(text)

        full_text = "\n\n".join(pages_text)

        # Collapse runs of 3+ blank lines into two (preserve paragraph breaks)
        full_text = re.sub(r"\n{3,}", "\n\n", full_text)
        # Collapse horizontal whitespace runs into a single space
        full_text = re.sub(r"[ \t]+", " ", full_text)

        return full_text.strip()

    except pdfplumber.pdfminer.pdfparser.PDFSyntaxError as e:
        raise ValueError(f"Corrupted or unreadable PDF: {file_path}") from e


def extract_text_from_docx(file_path: str) -> str:
    """Extract text from a .docx file using python-docx."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"DOCX file not found: {file_path}")

    try:
        doc = Document(file_path)
    except Exception as e:
        raise ValueError(f"Corrupted or unreadable DOCX: {file_path}") from e

    paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]

    if not paragraphs:
        raise ValueError(f"No readable text found in DOCX: {file_path}")

    full_text = "\n\n".join(paragraphs)
    full_text = re.sub(r"[ \t]+", " ", full_text)

    return full_text.strip()


def extract_text(file_path: str) -> str:
    """Detect file type by extension and delegate to the right parser."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    else:
        raise ValueError(
            f"Unsupported file type '{ext}'. Only .pdf and .docx are accepted."
        )
