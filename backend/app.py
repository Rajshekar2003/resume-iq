from flask import Flask, jsonify, request
from flask_cors import CORS

from routes.analyze import analyze_bp
from routes.extract_keywords import extract_keywords_bp
from routes.improve_bullet import improve_bullet_bp
from routes.market_analysis import market_analysis_bp
from routes.match import match_bp
from utils.file_handling import FileHandlingError, process_uploaded_resume

app = Flask(__name__)

# Allow all origins so the React frontend (any port) can call this API
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "https://resume-iq-indol.vercel.app",
            "https://resume-iq-rajshekarrc2003-7194s-projects.vercel.app",
            "https://*.vercel.app"
        ]
    }
})

app.register_blueprint(analyze_bp)
app.register_blueprint(extract_keywords_bp)
app.register_blueprint(improve_bullet_bp)
app.register_blueprint(market_analysis_bp)
app.register_blueprint(match_bp)


@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "service": "ai-resume-analyzer"})


@app.route("/api/upload", methods=["POST"])
def upload_resume():
    try:
        extracted_text = process_uploaded_resume(request)
        return jsonify({
            "success": True,
            "text_length": len(extracted_text),
            "extracted_text": extracted_text,
        })
    except FileHandlingError as e:
        return jsonify({"success": False, "error": str(e)}), e.status_code
    except Exception as e:
        return jsonify({"success": False, "error": f"Unexpected server error: {str(e)}"}), 500


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
