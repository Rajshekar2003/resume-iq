from flask import Blueprint, jsonify, request

from prompts.jd_match_prompt import JD_MATCH_PROMPT
from utils.file_handling import FileHandlingError, process_uploaded_resume
from utils.gemini_client import generate_structured_response
from utils.schemas import JdMatchResponse

match_bp = Blueprint("match_bp", __name__)

_JD_MIN_LENGTH = 50
_JD_MAX_LENGTH = 20_000


@match_bp.route("/api/match", methods=["POST"])
def match_resume():
    job_description = request.form.get("job_description", "").strip()

    if not job_description:
        return jsonify({"success": False, "error": "Missing field: job_description"}), 400
    if len(job_description) < _JD_MIN_LENGTH:
        return jsonify({"success": False, "error": f"job_description must be at least {_JD_MIN_LENGTH} characters"}), 400
    if len(job_description) > _JD_MAX_LENGTH:
        return jsonify({"success": False, "error": f"job_description must not exceed {_JD_MAX_LENGTH} characters"}), 400

    try:
        resume_text = process_uploaded_resume(request)
    except FileHandlingError as e:
        return jsonify({"success": False, "error": str(e)}), e.status_code

    try:
        prompt = JD_MATCH_PROMPT.format(resume_text=resume_text, job_description=job_description)
        result: JdMatchResponse = generate_structured_response(prompt, JdMatchResponse)
        return jsonify(result.model_dump())
    except RuntimeError as e:
        return jsonify({"success": False, "error": str(e)}), 500
    except Exception as e:
        return jsonify({"success": False, "error": f"Unexpected server error: {str(e)}"}), 500
