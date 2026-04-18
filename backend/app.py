import os
import tempfile

from flask import Flask, jsonify, request
from flask_cors import CORS

from utils.pdf_parser import extract_text

app = Flask(__name__)

# Allow all origins so the React frontend (any port) can call this API
CORS(app)

MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB
ALLOWED_EXTENSIONS = {".pdf", ".docx"}


@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "service": "ai-resume-analyzer"})


@app.route("/api/upload", methods=["POST"])
def upload_resume():
    if "resume" not in request.files:
        return jsonify({"success": False, "error": "No file field named 'resume' in request."}), 400

    file = request.files["resume"]

    if file.filename == "":
        return jsonify({"success": False, "error": "No file selected."}), 400

    _, ext = os.path.splitext(file.filename)
    ext = ext.lower()

    if ext not in ALLOWED_EXTENSIONS:
        return jsonify({
            "success": False,
            "error": f"Unsupported file type '{ext}'. Upload a .pdf or .docx file.",
        }), 400

    # Read into memory first so we can check size before touching the filesystem
    file_bytes = file.read()
    if len(file_bytes) > MAX_FILE_SIZE_BYTES:
        return jsonify({
            "success": False,
            "error": f"File too large ({len(file_bytes) // 1024} KB). Maximum allowed size is 5 MB.",
        }), 400

    # Use a named temp file so pdfplumber/docx can open it by path.
    # delete=False lets us close the file first; we remove it ourselves in finally.
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
            tmp.write(file_bytes)
            tmp_path = tmp.name

        extracted_text = extract_text(tmp_path)

        return jsonify({
            "success": True,
            "filename": file.filename,
            "text_length": len(extracted_text),
            "extracted_text": extracted_text,
        })

    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400

    except Exception as e:
        return jsonify({"success": False, "error": f"Unexpected server error: {str(e)}"}), 500

    finally:
        # Always remove the temp file — even if extraction failed
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
