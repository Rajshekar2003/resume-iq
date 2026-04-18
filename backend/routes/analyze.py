from flask import Blueprint, jsonify, request

from prompts.ats_score_prompt import ATS_SCORE_PROMPT
from utils.file_handling import FileHandlingError, process_uploaded_resume
from utils.gemini_client import generate_structured_response
from utils.schemas import AtsScoreResponse

analyze_bp = Blueprint("analyze_bp", __name__)


@analyze_bp.route("/api/analyze", methods=["POST"])
def analyze_resume():
    try:
        extracted_text = process_uploaded_resume(request)
    except FileHandlingError as e:
        return jsonify({"success": False, "error": str(e)}), e.status_code

    try:
        prompt = ATS_SCORE_PROMPT.format(resume_text=extracted_text)
        result: AtsScoreResponse = generate_structured_response(prompt, AtsScoreResponse)
        return jsonify(result.model_dump())
    except RuntimeError as e:
        return jsonify({"success": False, "error": str(e)}), 500
    except Exception as e:
        return jsonify({"success": False, "error": f"Unexpected server error: {str(e)}"}), 500
