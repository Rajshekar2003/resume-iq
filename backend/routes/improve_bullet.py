from flask import Blueprint, jsonify, request

from prompts.bullet_improver_prompt import BULLET_IMPROVER_PROMPT
from utils.gemini_client import generate_structured_response
from utils.schemas import BulletImprovementResponse

improve_bullet_bp = Blueprint("improve_bullet_bp", __name__)

_BULLET_MIN_LENGTH = 10
_BULLET_MAX_LENGTH = 500


@improve_bullet_bp.route("/api/improve-bullet", methods=["POST"])
def improve_bullet():
    if request.is_json:
        bullet_text = (request.get_json() or {}).get("bullet_text", "")
    else:
        bullet_text = request.form.get("bullet_text", "")
    bullet_text = bullet_text.strip()

    if not bullet_text:
        return jsonify({"success": False, "error": "Missing field: bullet_text"}), 400
    if len(bullet_text) < _BULLET_MIN_LENGTH:
        return jsonify({"success": False, "error": f"bullet_text must be at least {_BULLET_MIN_LENGTH} characters"}), 400
    if len(bullet_text) > _BULLET_MAX_LENGTH:
        return jsonify({"success": False, "error": f"bullet_text must not exceed {_BULLET_MAX_LENGTH} characters"}), 400

    try:
        prompt = BULLET_IMPROVER_PROMPT.format(bullet_text=bullet_text)
        result: BulletImprovementResponse = generate_structured_response(prompt, BulletImprovementResponse)
        return jsonify(result.model_dump())
    except RuntimeError as e:
        return jsonify({"success": False, "error": str(e)}), 500
    except Exception as e:
        return jsonify({"success": False, "error": f"Unexpected server error: {str(e)}"}), 500
