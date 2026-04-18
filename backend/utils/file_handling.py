import os
import tempfile

from flask import Request

from utils.pdf_parser import extract_text

MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024
ALLOWED_EXTENSIONS = {".pdf", ".docx"}


class FileHandlingError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.status_code = status_code


def process_uploaded_resume(request: Request) -> str:
    if "resume" not in request.files:
        raise FileHandlingError("No file field named 'resume' in request.")

    file = request.files["resume"]

    if file.filename == "":
        raise FileHandlingError("No file selected.")

    _, ext = os.path.splitext(file.filename)
    ext = ext.lower()

    if ext not in ALLOWED_EXTENSIONS:
        raise FileHandlingError(
            f"Unsupported file type '{ext}'. Upload a .pdf or .docx file."
        )

    file_bytes = file.read()
    if len(file_bytes) > MAX_FILE_SIZE_BYTES:
        raise FileHandlingError(
            f"File too large ({len(file_bytes) // 1024} KB). Maximum allowed size is 5 MB."
        )

    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
            tmp.write(file_bytes)
            tmp_path = tmp.name

        return extract_text(tmp_path)

    except FileHandlingError:
        raise
    except ValueError as e:
        raise FileHandlingError(str(e)) from e
    except Exception as e:
        raise FileHandlingError(f"Unexpected server error: {str(e)}", status_code=500) from e
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)
