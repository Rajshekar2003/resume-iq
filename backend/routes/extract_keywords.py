from flask import Blueprint, jsonify, request

from prompts.keyword_extraction_prompt import KEYWORD_EXTRACTION_PROMPT
from utils.gemini_client import generate_structured_response
from utils.schemas import KeywordExtractionResponse

extract_keywords_bp = Blueprint("extract_keywords_bp", __name__)

_JD_MIN_LENGTH = 50
_JD_MAX_LENGTH = 20_000


@extract_keywords_bp.route("/api/extract-keywords", methods=["POST"])
def extract_keywords():
    if request.is_json:
        job_description = (request.get_json() or {}).get("job_description", "")
    else:
        job_description = request.form.get("job_description", "")
    job_description = job_description.strip()

    if not job_description:
        return jsonify({"success": False, "error": "Missing field: job_description"}), 400
    if len(job_description) < _JD_MIN_LENGTH:
        return jsonify({"success": False, "error": f"job_description must be at least {_JD_MIN_LENGTH} characters"}), 400
    if len(job_description) > _JD_MAX_LENGTH:
        return jsonify({"success": False, "error": f"job_description must not exceed {_JD_MAX_LENGTH} characters"}), 400

    try:
        prompt = KEYWORD_EXTRACTION_PROMPT.format(job_description=job_description)
        result: KeywordExtractionResponse = generate_structured_response(prompt, KeywordExtractionResponse)
        return jsonify(result.model_dump())
    except RuntimeError as e:
        return jsonify({"success": False, "error": str(e)}), 500
    except Exception as e:
        return jsonify({"success": False, "error": f"Unexpected server error: {str(e)}"}), 500
