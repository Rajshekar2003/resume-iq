import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))


def _get_client() -> genai.GenerativeModel:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your_key_here":
        raise EnvironmentError(
            "GEMINI_API_KEY is not set. Add your key to backend/.env"
        )
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.5-flash")


def generate_text(prompt: str) -> str:
    try:
        model = _get_client()
        response = model.generate_content(prompt)
        return response.text
    except EnvironmentError:
        raise
    except Exception as e:
        raise RuntimeError(f"Gemini API call failed: {e}") from e
